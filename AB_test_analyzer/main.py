from validator import DataValidator
from analyzer import ABAnalyzer


def main() -> None:
    # Step 1: Validate data
    validator = DataValidator("test_in_50.csv")
    validator.validate()

    # Step 2: Retrieve validated data
    valid_data = validator.get_valid_data()
    errors = validator.get_errors()

    # Step 3: Display validation results
    print(f"Valid records: {len(valid_data)}")
    print(f"Validation errors: {len(errors)}")

    # Step 4: Initialize analyzer
    analyzer = ABAnalyzer(valid_data)

    if not analyzer.A or not analyzer.B:
        print("Error: Both groups must contain observations.")
        return

    if analyzer.standard_error() == 0:
        print("Error: Standard error is zero.")
        return

    # Step 5: Perform statistical analysis
    p_A, p_B = analyzer.conversion_rates()
    z, p_value = analyzer.z_test()

    # Step 6: Display results
    print("\n=== A/B Testing Results ===")
    print(f"Group A conversion rate: {p_A:.2%}")
    print(f"Group B conversion rate: {p_B:.2%}")
    print(f"Z statistic: {z:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Conclusion: {analyzer.interpret()}")


if __name__ == "__main__":
    main()
