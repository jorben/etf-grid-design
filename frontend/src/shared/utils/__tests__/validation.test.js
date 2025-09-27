import {
  validateETFCode,
  validateCapital,
  validatePercentage,
  validateDate,
  validateRequired,
  validateNumberRange,
  validateForm,
} from "../validation";

describe("validation utils", () => {
  describe("validateETFCode", () => {
    test("should validate 6-digit ETF codes", () => {
      expect(validateETFCode("510300")).toBe(true);
      expect(validateETFCode("000001")).toBe(true);
      expect(validateETFCode("999999")).toBe(true);
    });

    test("should reject invalid ETF codes", () => {
      expect(validateETFCode("123")).toBe(false);
      expect(validateETFCode("1234567")).toBe(false);
      expect(validateETFCode("abc123")).toBe(false);
      expect(validateETFCode("")).toBe(false);
      expect(validateETFCode(null)).toBe(false);
      expect(validateETFCode(undefined)).toBe(false);
    });
  });

  describe("validateCapital", () => {
    test("should validate capital within range", () => {
      expect(validateCapital(100000)).toEqual({ isValid: true, error: "" });
      expect(validateCapital(500000)).toEqual({ isValid: true, error: "" });
      expect(validateCapital(5000000)).toEqual({ isValid: true, error: "" });
    });

    test("should reject capital below minimum", () => {
      expect(validateCapital(99999)).toEqual({
        isValid: false,
        error: "投资金额不能少于10万元",
      });
      expect(validateCapital(0)).toEqual({
        isValid: false,
        error: "投资金额不能少于10万元",
      });
    });

    test("should reject capital above maximum", () => {
      expect(validateCapital(5000001)).toEqual({
        isValid: false,
        error: "投资金额不能超过500万元",
      });
    });

    test("should reject invalid input", () => {
      expect(validateCapital("invalid")).toEqual({
        isValid: false,
        error: "请输入有效的投资金额",
      });
      expect(validateCapital(NaN)).toEqual({
        isValid: false,
        error: "请输入有效的投资金额",
      });
      expect(validateCapital(null)).toEqual({
        isValid: false,
        error: "请输入有效的投资金额",
      });
    });
  });

  describe("validatePercentage", () => {
    test("should validate percentage within range", () => {
      expect(validatePercentage(0)).toEqual({ isValid: true, error: "" });
      expect(validatePercentage(0.5)).toEqual({ isValid: true, error: "" });
      expect(validatePercentage(1)).toEqual({ isValid: true, error: "" });
    });

    test("should validate with custom range", () => {
      expect(validatePercentage(0.1, { min: 0.1, max: 0.9 })).toEqual({
        isValid: true,
        error: "",
      });
      expect(validatePercentage(0.05, { min: 0.1, max: 0.9 })).toEqual({
        isValid: false,
        error: "百分比值不能小于10%",
      });
    });

    test("should reject invalid input", () => {
      expect(validatePercentage("invalid")).toEqual({
        isValid: false,
        error: "请输入有效的百分比值",
      });
    });
  });

  describe("validateDate", () => {
    test("should validate YYYY-MM-DD format", () => {
      expect(validateDate("2024-03-15")).toEqual({ isValid: true, error: "" });
      expect(validateDate("2024-12-25")).toEqual({ isValid: true, error: "" });
    });

    test("should validate YYYYMMDD format", () => {
      expect(validateDate("20240315", "YYYYMMDD")).toEqual({
        isValid: true,
        error: "",
      });
      expect(validateDate("20241225", "YYYYMMDD")).toEqual({
        isValid: true,
        error: "",
      });
    });

    test("should reject invalid dates", () => {
      expect(validateDate("2024-13-01")).toEqual({
        isValid: false,
        error: "请输入有效的日期",
      });
      expect(validateDate("2024-02-30")).toEqual({
        isValid: false,
        error: "请输入有效的日期",
      });
    });

    test("should reject empty input", () => {
      expect(validateDate("")).toEqual({
        isValid: false,
        error: "请输入日期",
      });
    });
  });

  describe("validateRequired", () => {
    test("should validate required fields", () => {
      expect(validateRequired("value", "字段名")).toEqual({
        isValid: true,
        error: "",
      });
      expect(validateRequired(0, "字段名")).toEqual({
        isValid: true,
        error: "",
      });
      expect(validateRequired(false, "字段名")).toEqual({
        isValid: true,
        error: "",
      });
    });

    test("should reject empty fields", () => {
      expect(validateRequired("", "ETF代码")).toEqual({
        isValid: false,
        error: "ETF代码是必填项",
      });
      expect(validateRequired(null, "投资金额")).toEqual({
        isValid: false,
        error: "投资金额是必填项",
      });
      expect(validateRequired(undefined, "频率偏好")).toEqual({
        isValid: false,
        error: "频率偏好是必填项",
      });
    });
  });

  describe("validateNumberRange", () => {
    test("should validate numbers within range", () => {
      expect(validateNumberRange(50, { min: 0, max: 100 }, "年龄")).toEqual({
        isValid: true,
        error: "",
      });
    });

    test("should reject numbers outside range", () => {
      expect(validateNumberRange(-1, { min: 0, max: 100 }, "年龄")).toEqual({
        isValid: false,
        error: "年龄不能小于0",
      });
      expect(validateNumberRange(101, { min: 0, max: 100 }, "年龄")).toEqual({
        isValid: false,
        error: "年龄不能大于100",
      });
    });

    test("should reject invalid input", () => {
      expect(
        validateNumberRange("invalid", { min: 0, max: 100 }, "年龄"),
      ).toEqual({
        isValid: false,
        error: "年龄必须是有效的数字",
      });
    });
  });

  describe("validateForm", () => {
    test("should validate form data with multiple rules", () => {
      const formData = {
        etfCode: "510300",
        totalCapital: 100000,
      };

      const rules = {
        etfCode: [validateRequired, validateETFCode],
        totalCapital: [validateRequired, validateCapital],
      };

      const result = validateForm(formData, rules);
      expect(result.isValid).toBe(true);
      expect(result.errors).toEqual({});
    });

    test("should return errors for invalid form data", () => {
      const formData = {
        etfCode: "123",
        totalCapital: 5000,
      };

      const rules = {
        etfCode: [validateRequired, validateETFCode],
        totalCapital: [validateRequired, validateCapital],
      };

      const result = validateForm(formData, rules);
      expect(result.isValid).toBe(false);
      expect(result.errors.etfCode).toBeDefined();
      expect(result.errors.totalCapital).toBeDefined();
    });

    test("should handle empty form data", () => {
      const formData = {};
      const rules = {
        etfCode: [validateRequired],
        totalCapital: [validateRequired],
      };

      const result = validateForm(formData, rules);
      expect(result.isValid).toBe(false);
      expect(result.errors.etfCode).toBe("ETF代码是必填项");
      expect(result.errors.totalCapital).toBe("投资金额是必填项");
    });
  });
});
