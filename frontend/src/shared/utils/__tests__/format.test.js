import {
  formatCurrency,
  formatPercent,
  formatDate,
  formatNumber,
  formatLargeNumber,
} from "../format";

describe("format utils", () => {
  describe("formatCurrency", () => {
    test("should format numbers correctly", () => {
      expect(formatCurrency(100000)).toBe("¥100,000");
      expect(formatCurrency(1234567)).toBe("¥1,234,567");
      expect(formatCurrency(1234.56)).toBe("¥1,235");
    });

    test("should handle decimal options", () => {
      expect(
        formatCurrency(1234.56, {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2,
        }),
      ).toBe("¥1,234.56");
      expect(formatCurrency(1234.567, { maximumFractionDigits: 2 })).toBe(
        "¥1,234.57",
      );
    });

    test("should throw error for invalid input", () => {
      expect(() => formatCurrency("invalid")).toThrow(
        "Amount must be a valid number",
      );
      expect(() => formatCurrency(NaN)).toThrow(
        "Amount must be a valid number",
      );
    });

    test("should handle edge cases", () => {
      expect(formatCurrency(0)).toBe("¥0");
      expect(formatCurrency(-1000)).toBe("-¥1,000");
    });
  });

  describe("formatPercent", () => {
    test("should format decimals correctly", () => {
      expect(formatPercent(0.1234)).toBe("12.34%");
      expect(formatPercent(0.05)).toBe("5.00%");
      expect(formatPercent(1)).toBe("100.00%");
    });

    test("should handle custom digits", () => {
      expect(formatPercent(0.1234, 1)).toBe("12.3%");
      expect(formatPercent(0.05, 0)).toBe("5%");
    });

    test("should throw error for invalid input", () => {
      expect(() => formatPercent("invalid")).toThrow(
        "Value must be a valid number",
      );
      expect(() => formatPercent(NaN)).toThrow("Value must be a valid number");
    });

    test("should handle edge cases", () => {
      expect(formatPercent(0)).toBe("0.00%");
      expect(formatPercent(-0.1)).toBe("-10.00%");
    });
  });

  describe("formatDate", () => {
    test("should handle YYYYMMDD format", () => {
      expect(formatDate("20240315")).toBe("2024-03-15");
      expect(formatDate("20241225")).toBe("2024-12-25");
    });

    test("should handle YYYY-MM-DD format", () => {
      expect(formatDate("2024-03-15")).toBe("2024-03-15");
      expect(formatDate("2024-12-25")).toBe("2024-12-25");
    });

    test("should return null for invalid input", () => {
      expect(formatDate("")).toBe(null);
      expect(formatDate(null)).toBe(null);
      expect(formatDate(undefined)).toBe(null);
      expect(formatDate("invalid")).toBe(null);
      expect(formatDate("2024")).toBe(null);
    });
  });

  describe("formatNumber", () => {
    test("should format numbers with thousand separators", () => {
      expect(formatNumber(1000000)).toBe("1,000,000");
      expect(formatNumber(1234.56)).toBe("1,234.56");
      expect(formatNumber(123)).toBe("123");
    });

    test("should handle invalid input", () => {
      expect(formatNumber("invalid")).toBe("0");
      expect(formatNumber(NaN)).toBe("0");
    });

    test("should handle edge cases", () => {
      expect(formatNumber(0)).toBe("0");
      expect(formatNumber(-1234)).toBe("-1,234");
    });
  });

  describe("formatLargeNumber", () => {
    test("should format numbers in 万 units", () => {
      expect(formatLargeNumber(10000)).toBe("1.00万");
      expect(formatLargeNumber(12345)).toBe("1.23万");
      expect(formatLargeNumber(99999)).toBe("10.00万");
    });

    test("should format numbers in 亿 units", () => {
      expect(formatLargeNumber(100000000)).toBe("1.00亿");
      expect(formatLargeNumber(123456789)).toBe("1.23亿");
    });

    test("should handle numbers below 10000", () => {
      expect(formatLargeNumber(1000)).toBe("1,000");
      expect(formatLargeNumber(9999)).toBe("9,999");
    });

    test("should handle invalid input", () => {
      expect(formatLargeNumber("invalid")).toBe("0");
      expect(formatLargeNumber(NaN)).toBe("0");
    });

    test("should handle edge cases", () => {
      expect(formatLargeNumber(0)).toBe("0");
      expect(formatLargeNumber(-10000)).toBe("-1.00万");
    });
  });
});
