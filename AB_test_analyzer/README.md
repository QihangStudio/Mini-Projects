# A/B Test Analyzer

A lightweight Python project for validating A/B experiment data and comparing conversion rates with a **two-sided, two-proportion Z-test**. It separates CSV validation, statistical analysis, and reporting, and includes unit tests, a regression test, and a Jupyter notebook for exploring results.

## Features

- Reads experiment records from CSV (`user_id`, `group`, `converted`).
- Validates missing fields, group labels (`A` or `B`), and conversion values (`0` or `1`).
- **Excludes every record associated with a duplicated user ID**, rather than keeping the first occurrence.
- Computes conversion rates, pooled proportion, standard error, Z statistic, and two-sided p-value.
- Reports whether to reject the null hypothesis at a configurable significance level (default `0.05`).
- Supports automated unit and full-program output comparison tests.

## Project structure

```text
AB_test_analyzer/
├── analyzer.py                        # Statistical calculations
├── validator.py                       # CSV data validation
├── main.py                            # Command-line entry point
├── test_in_50.csv                     # Example test dataset
├── test_main_unit.py                  # Unit tests
├── test_main_reg.py                   # Output regression test
├── test_validator.py                  # Additional validator tests, if present
├── expected_output.txt                # Reviewed regression-test baseline
├── AB_Testing_Quick_Analysis.ipynb    # Interactive walkthrough
└── README.md
```

## Requirements

- Python 3.10+ (3.13 is also supported by the project's basic syntax)
- NumPy
- SciPy
- Matplotlib (for the notebook chart)
- Jupyter or the VS Code Jupyter extension (to run the notebook)

Install the required Python packages:

```bash
python3 -m pip install numpy scipy matplotlib jupyter
```

## Input format

The input CSV must contain the following columns:

| Column | Meaning | Allowed values |
| --- | --- | --- |
| `user_id` | Unique user identifier | Nonempty string |
| `group` | Experiment assignment | `A` or `B` |
| `converted` | Binary conversion outcome | `0` or `1` |

Example:

```csv
user_id,group,converted
U001,A,1
U002,A,0
U003,B,1
U004,B,0
```

**Important:** Duplicate IDs are identified across the entire CSV. All rows for duplicated IDs are excluded from the analysis, even if their group assignments differ.

## Run the analysis

From the project folder:

```bash
python3 main.py
```

Make sure the `DataValidator(...)` path in `main.py` points to your actual CSV file. For the included fixture, use:

```python
validator = DataValidator("test_in_50.csv")
```

To save the terminal output:

```bash
python3 main.py > actual_output.txt
```

For the provided 50-record fixture, the expected summary is:

```text
Valid records: 41
Validation errors: 9

=== A/B Testing Results ===
Group A conversion rate: 50.00%
Group B conversion rate: 61.90%
Z statistic: 0.7678
P-value: 0.4426
Conclusion: Fail to reject H0. No statistically significant difference between A and B.
```

## Statistical method

Let `x_A`, `x_B` be converted users and `n_A`, `n_B` be total valid users in groups A and B.

Conversion rates:

$$
\hat p_A=\frac{x_A}{n_A},\qquad \hat p_B=\frac{x_B}{n_B}
$$

Under the null hypothesis $H_0:p_A=p_B$, the pooled conversion rate and standard error are:

$$
\hat p=\frac{x_A+x_B}{n_A+n_B},\qquad
SE=\sqrt{\hat p(1-\hat p)\left(\frac1{n_A}+\frac1{n_B}\right)}
$$

The test statistic and two-sided p-value are:

$$
Z=\frac{\hat p_B-\hat p_A}{SE},\qquad
p\text{-value}=2\bigl(1-\Phi(|Z|)\bigr)
$$

If the p-value is below `alpha`, reject $H_0$; otherwise, **fail to reject** $H_0$. Failing to reject does not prove the conversion rates are equal.

**Limitations:** The Z-test assumes independent observations and sufficiently large expected success/failure counts for the normal approximation to be reasonable. The 50-row CSV is intended mainly to test the software, not to support a strong real-world inference. The standard error is zero if every valid observation is `0` or every observation is `1`; the current CLI checks that case before running the Z-test.

## Testing

Run all tests from the project folder:

```bash
python3 -m unittest discover -s . -p "test_*.py" -v
```

The unit tests validate record filtering and statistical calculations. The regression test runs `main.py` and checks its **exact standard output** against `expected_output.txt` (including spacing, number formatting, and the final newline). Ensure the file exists and was reviewed before using it as a baseline. If you change the input data or output format intentionally, verify the new result before updating the baseline.

## Jupyter notebook

Open `AB_Testing_Quick_Analysis.ipynb` from the project directory and run the cells in order. The notebook reuses `DataValidator` and `ABAnalyzer` to show validation issues, group conversion rates, the Z-test result, and a simple bar chart.

## Optional cleanup

Python does not require compiling this project. To remove local Python bytecode caches:

```bash
find . -type d -name "__pycache__" -prune -exec rm -rf {} +
```

Keep `expected_output.txt` under version control; consider ignoring `__pycache__/`, `*.pyc`, and `actual_output.txt`.
