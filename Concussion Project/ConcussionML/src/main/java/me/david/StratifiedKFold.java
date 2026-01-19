package me.david;

import org.apache.commons.csv.CSVFormat;
import smile.classification.RandomForest;
import smile.data.DataFrame;
import smile.data.Row;
import smile.data.formula.Formula;
import smile.data.vector.ValueVector;
import smile.io.Read;
import smile.validation.Bag;
import smile.validation.ClassificationMetrics;
import smile.validation.ClassificationValidations;
import smile.validation.CrossValidation;
import smile.validation.metric.ConfusionMatrix;

import java.io.File;
import java.io.FileWriter;
import java.util.*;
import java.util.function.BiFunction;
import java.util.stream.IntStream;

public class StratifiedKFold {
    public static void main(String[] args) throws Exception {
        DataFrame rawData = Read.csv("C:\\Users\\PL003A\\Desktop\\Concussion Analysis\\ConcussionML\\src\\main\\resources\\all.csv",
                CSVFormat.DEFAULT.withFirstRecordAsHeader());
        DataFrame data = preProcess(rawData, "mean");
        data = data.drop("GENDER", "SessionName", "ID");

        Formula formula = Formula.lhs("CONCUSSED");
        int k = 5;
        int trials = 1000;
        int featureCount = data.ncol() - 1;

        double totalAcc = 0, totalPrec = 0, totalF1 = 0;
        double[] importances = new double[featureCount];
        List<String> featureList = new ArrayList<>();
        int[][] confusionMatrix = new int[2][2];

        List<Double> f1Scores = new ArrayList<>();

        for (int t = 0; t < trials; t++) {
            BiFunction<Formula, DataFrame, RandomForest> trainer = (f, d) -> {
                RandomForest.Options options = new RandomForest.Options(
                        500,
                        featureCount/3,
                        20,
                        0,
                        1
                );

                return RandomForest.fit(f, d, options);
            };

            ClassificationValidations<RandomForest> results =
                    CrossValidation.stratify(k, formula, data, trainer);

            totalAcc += results.avg().accuracy();
            totalPrec += results.avg().precision();
            totalF1 += results.avg().f1();

            System.out.println("\nMetrics per fold:");
            for (int i = 0; i < results.rounds().size(); i++) {
                System.out.println(results.rounds().get(i).confusion());
                ClassificationMetrics m = results.rounds().get(i).metrics();
                System.out.printf("Fold %d - Acc: %.4f, Prec: %.4f, F1: %.4f\n",
                        i + 1, m.accuracy(), m.precision(), m.f1());

                f1Scores.add(m.f1());

                for (int j = 0; j < results.rounds().get(i).model().importance().length; j++)
                    importances[j] += results.rounds().get(i).model().importance()[j];


                for (int j = 0; j < 2; j++) for (int f = 0; f < 2; f++)
                    confusionMatrix[j][f] += results.rounds().get(i).confusion().matrix()[j][f];
            }

            if (t == 0)
                featureList = Arrays.asList(data.drop("CONCUSSED").names());
        }

        System.out.println("\n--------");
        System.out.println("Summed Confusion Matrix:");
        System.out.println("\tPredicted 0\tPredicted 1");
        System.out.printf("Actual 0\t%d\t\t%d\n", confusionMatrix[0][0], confusionMatrix[0][1]);
        System.out.printf("Actual 1\t%d\t\t%d\n", confusionMatrix[1][0], confusionMatrix[1][1]);

        System.out.println("\nFinal Averages over " + (k * trials) + " folds");
        System.out.printf("Accuracy : %.4f\n", totalAcc / trials);
        System.out.printf("Precision: %.4f\n", totalPrec / trials);
        System.out.printf("F1 Score : %.4f\n", totalF1 / trials);

        System.out.println("\nAverage Feature Importances");
        Map<Double, Integer> originalIndex = new HashMap<>();
        for (int i = 0; i < importances.length; i++)
            originalIndex.put((importances[i]/(trials * k)), i);
        Arrays.sort(importances);

        System.out.println("\nFinal Averaged Importances");
        for (int i = importances.length - 1; i >= 0; i--)
            System.out.println(featureList.get(originalIndex.get(importances[i]/(trials * k))) + ": " + importances[i]/(trials * k));


        File f1ScoresFile = new File("f1Scores.txt");
        f1ScoresFile.createNewFile();
        FileWriter writer = new FileWriter(f1ScoresFile);
        writer.write(f1Scores.toString());
        writer.close();
    }

    private static DataFrame preProcess(DataFrame raw, String imputationMethod) {
        ValueVector genderColumn = raw.column("GENDER");

        for (int i = 0; i < genderColumn.size(); i++)
            genderColumn.set(i, genderColumn.get(i).toString().substring(0, 1));

        raw.set("GENDER", genderColumn);

        Map<String, Double[]> columnAverages = new HashMap<>();
        for (String col : raw.names()) {
            if (col.equals("CONCUSSED") || col.equals("GENDER") || col.equals("SessionName")) continue;
            Double[] classAverages = new Double[2];

            for (int i = 0; i <= 1; i++) { // Loop through Concussed and Non Concussed
                int concussedState = i;
                List<Row> filteredRows = raw.stream().filter(row -> row.getInt("CONCUSSED") == concussedState).toList();

                double sum = 0;
                int totalNaNs = 0;

                for (Row row : filteredRows) {
                    double parsed = Double.parseDouble(row.getString(col));
                    if (!Double.isNaN(parsed)) sum += Double.parseDouble(row.getString(col));
                    else totalNaNs++;
                }

                System.out.println("Average for Column " + col + ": " + (sum/(filteredRows.size()-totalNaNs)));
                classAverages[i] = (sum/(filteredRows.size()-totalNaNs));
            }

            columnAverages.put(col, classAverages);
        }

        for (String col : raw.names()) {
            if (col.equals("CONCUSSED") || col.equals("GENDER") || col.equals("SessionName")) continue;
            ValueVector updatedVector = raw.column(col);

            for (Row row : raw) {
                int concussed = row.getInt("CONCUSSED");
                if (Double.isNaN(Double.parseDouble(row.getString(col))))
                    updatedVector.set(row.index(), columnAverages.get(col)[concussed].toString());
            }

            raw.set(col, updatedVector);
        }

        int[] ids = IntStream.range(0, raw.nrow()).toArray();
        raw.add(ValueVector.of("ID", ids));
        raw = raw.setIndex("ID");

        return raw;
    }
}
