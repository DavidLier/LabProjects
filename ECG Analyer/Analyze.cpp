#include <winsock2.h>
#include <windowsx.h>
#include <windows.h>
#include <iostream>
#include <chrono>
#include <thread>
#include <queue>
#include <mutex>
#include <condition_variable>

#pragma comment(lib, "ws2_32.lib")

#include "ScheduledSignal.cpp"


HDC g_hdcMem = NULL;
HBITMAP g_hdcBitmap = NULL;

const char g_szClassName[] = "ECGScanner";

// Assuming full screen of Biopac software on main monitor, might in the future makes this adjustable in the client but realistically we only ever record on that computer
// since it has the ethernet cable connected to the other
const int srcX = 1791;
const int srcY = 450;

const int captureWidth = 1;
const int captureHeight = 150;

int threshold = 15;

DWORD strip[250][350];
int currentCol = 0;

WSADATA wsa;
SOCKET sock;
sockaddr_in dest;

const char* ip = "169.254.221.3";
int port = 5005;

int lastHeight = -999;

int offset = -50;

std::chrono::steady_clock::time_point lastQRSComplexTime;

std::priority_queue<ScheduledSignal> signals;
std::mutex signalMutex;
std::condition_variable signalCV;

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam);
void analyzeStrip(HDC& hdcScreen, BYTE* pixelData, BITMAPINFO& bmi);
void sendUDP(const char* message);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE, LPSTR, int nCmdShow) {
    WSAStartup(MAKEWORD(2, 2), &wsa);
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == INVALID_SOCKET) {
        WSACleanup();
        return -1;
    }

    dest.sin_family = AF_INET;
    dest.sin_port = htons(port);
    dest.sin_addr.s_addr = inet_addr(ip);

    WNDCLASS wc = {};
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = g_szClassName;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 2);

    RegisterClass(&wc);

    HWND hwnd = CreateWindowEx(
        0, g_szClassName, "ECG Stimuli Sender",
        WS_OVERLAPPEDWINDOW ^ WS_THICKFRAME ^ WS_MAXIMIZEBOX,
        CW_USEDEFAULT, CW_USEDEFAULT, 300, 300,
        NULL, NULL, hInstance, NULL);

    if (!hwnd) return 1;

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    std::thread udpThread([]() {
        while (true) {
            std::unique_lock<std::mutex> lock(signalMutex);
            if (signals.empty()) {
                signalCV.wait(lock);  
                continue;
            }

            auto now = std::chrono::steady_clock::now();
            auto& next = signals.top();

            if (next.scheduledTime <= now) {
                for (int i = 0; i < threshold; i++)
                    strip[currentCol - 1][i] = RGB(0, 0, 255);

                sendUDP(next.signal.c_str()); 
                signals.pop();
            } else {
                signalCV.wait_until(lock, next.scheduledTime);
            }
        }
    });

    udpThread.detach();

    HDC hdcScreen = GetDC(NULL);
    g_hdcMem = CreateCompatibleDC(hdcScreen);
    g_hdcBitmap = CreateCompatibleBitmap(hdcScreen, captureWidth, captureHeight);
    SelectObject(g_hdcMem, g_hdcBitmap);

    BYTE* pixelData = new BYTE[captureWidth * captureHeight * 4];

    BITMAPINFO bmi = {};
    bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    bmi.bmiHeader.biWidth = captureWidth;
    bmi.bmiHeader.biHeight = -captureHeight;
    bmi.bmiHeader.biPlanes = 1;
    bmi.bmiHeader.biBitCount = 32;
    bmi.bmiHeader.biCompression = BI_RGB;

    std::chrono::duration<double> frameTime(1.0 / 240.0);
    while (true) {
        auto startTime = std::chrono::high_resolution_clock::now();

        analyzeStrip(hdcScreen, pixelData, bmi);
        InvalidateRect(hwnd, NULL, FALSE);

        MSG msg = {};
        while (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }

        auto endTime = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsedTime = endTime - startTime;

        if (elapsedTime < frameTime) {
            std::this_thread::sleep_for(frameTime - elapsedTime);
        }
    }

    DeleteObject(g_hdcBitmap);
    DeleteDC(g_hdcMem);
    ReleaseDC(NULL, hdcScreen);

    return 0;
}

void analyzeStrip(HDC& hdcScreen, BYTE* pixelData, BITMAPINFO& bmi) {
    BitBlt(g_hdcMem, 0, 0, captureWidth, captureHeight, hdcScreen, srcX, srcY, SRCCOPY);

    int success = GetDIBits(
        g_hdcMem,
        g_hdcBitmap,
        0,
        captureHeight,
        pixelData,
        &bmi,
        DIB_RGB_COLORS
    );

    if (success == 0) 
        return;

    if (currentCol == 250) currentCol = 0;

    int currentHeight = -1;
    for (int y = captureHeight; y > 0; --y) {
        int i = y * captureWidth * 4;
        BYTE b = pixelData[i + 0];
        BYTE g = pixelData[i + 1];
        BYTE r = pixelData[i + 2];

        // Vagualy purple color, this range seems to work perfectly since there's the different gradients of color that pop up due to the filter lines on the screen
        if (r > 120 && b > 120 && g < std::min(r, b) - 40) {
            currentHeight = y;

            if (currentHeight != lastHeight) {
                lastHeight = y;
            }

            strip[currentCol][y] = RGB(r, g, b);
            if (y <= threshold) strip[currentCol][y] = RGB(255, 255, 255);
            continue;
        }

        strip[currentCol][y] = RGB(0, 0, 0);
    }

    currentCol++;

    // CROSSED QRS
    if (currentHeight <= threshold) {
        auto now = std::chrono::steady_clock::now();

        // Allows for a buffer between signals, we don't have a reason to get them so quickly anyway
        // Mitigates signals getting dropped but realistically that doesn't have any affect on the end result anyway.
        if ((now - lastQRSComplexTime) < std::chrono::milliseconds(1000)) 
            return;

        lastQRSComplexTime = now;

        {
            std::lock_guard<std::mutex> lock(signalMutex);
            signals.push(ScheduledSignal("Systolic", now + std::chrono::milliseconds(200 + offset))); // Matches Previous Literature UPDATED TO 200, LAST 100 PARTICIPANT WAS P299
            signals.push(ScheduledSignal("Diastolic", now + std::chrono::milliseconds(500 + offset))); // https://www.sciencedirect.com/science/article/pii/S0960982223001744?via%3Dihub
        }

        signalCV.notify_one();
    }
}


LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);

            StretchBlt(hdc,
                0, 0, captureWidth * 4, captureHeight * 2,  
                g_hdcMem,
                0, 0, captureWidth, captureHeight,
                SRCCOPY);

            const int width = 250;
            const int height = captureHeight;
            BYTE pixels[height][width][4];

            for (int y = 0; y < height; ++y) {
                for (int x = 0; x < width; ++x) {
                    DWORD color = strip[x][y];

                    pixels[y][x][0] = GetBValue(color);
                    pixels[y][x][1] = GetGValue(color);
                    pixels[y][x][2] = GetRValue(color);
                    pixels[y][x][3] = 255;
                }
            }

            BITMAPINFO bmi = {};
            bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
            bmi.bmiHeader.biWidth = width;
            bmi.bmiHeader.biHeight = -height;
            bmi.bmiHeader.biPlanes = 1;
            bmi.bmiHeader.biBitCount = 32;
            bmi.bmiHeader.biCompression = BI_RGB;

            // Draw the strip
            SetDIBitsToDevice(
                hdc,
                5, 0, width, height,
                0, 0, 0, height,
                pixels,
                &bmi,
                DIB_RGB_COLORS
            );


            // Draw the threshold line
            HPEN hPen = CreatePen(PS_SOLID, 1, RGB(255, 0, 0));
            HPEN hOldPen = (HPEN)SelectObject(hdc, hPen);

            MoveToEx(hdc, 5, threshold, NULL);
            LineTo(hdc, width, threshold);

            SelectObject(hdc, hOldPen);
            DeleteObject(hPen);

            EndPaint(hwnd, &ps);
            return 0;
        }

        case WM_LBUTTONDOWN: // Figured the easiest method would be to just update the threshold line on click
            threshold = GET_Y_LPARAM(lParam);
            InvalidateRect(hwnd, NULL, FALSE);
            break;
        case WM_CLOSE:
            DestroyWindow(hwnd);
            break;

        case WM_DESTROY:
            PostQuitMessage(0);
            break;

        default:
            return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

void sendUDP(const char* message) {
    sendto(sock, message, strlen(message), 0, (sockaddr*)&dest, sizeof(dest));
}
