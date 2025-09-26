import { renderHook, act } from "@testing-library/react";
import {
  useShare,
  canUseWebShare,
  canUseClipboard,
  getShareCapabilities,
} from "../useShare";

// Mock navigator.share and navigator.clipboard
const mockNavigator = {
  share: jest.fn(),
  canShare: jest.fn(),
  clipboard: {
    writeText: jest.fn(),
  },
};

// Mock window.prompt and alert
global.prompt = jest.fn();
global.alert = jest.fn();

// Mock document.execCommand
document.execCommand = jest.fn();

beforeEach(() => {
  jest.clearAllMocks();
  Object.defineProperty(global, "navigator", {
    value: mockNavigator,
    writable: true,
  });
});

describe("useShare", () => {
  test("should return shareContent function", () => {
    const { result } = renderHook(() => useShare());
    expect(typeof result.current.shareContent).toBe("function");
  });

  describe("shareContent function", () => {
    test("should use Web Share API when available", async () => {
      mockNavigator.share.mockResolvedValue();
      mockNavigator.canShare.mockReturnValue(true);

      const { result } = renderHook(() => useShare());
      const shareData = {
        title: "Test Title",
        text: "Test Text",
        url: "https://example.com",
      };

      await act(async () => {
        const shareResult = await result.current.shareContent(shareData);
        expect(shareResult).toEqual({ success: true, method: "native" });
      });

      expect(mockNavigator.share).toHaveBeenCalledWith(shareData);
    });

    test("should fallback to clipboard when Web Share fails", async () => {
      mockNavigator.share.mockRejectedValue(new Error("Share cancelled"));
      mockNavigator.canShare.mockReturnValue(true);
      mockNavigator.clipboard.writeText.mockResolvedValue();

      const { result } = renderHook(() => useShare());
      const shareData = { url: "https://example.com" };

      await act(async () => {
        const shareResult = await result.current.shareContent(shareData);
        expect(shareResult).toEqual({ success: true, method: "clipboard" });
      });

      expect(mockNavigator.clipboard.writeText).toHaveBeenCalledWith(
        "https://example.com",
      );
      expect(alert).toHaveBeenCalledWith("链接已复制到剪贴板！");
    });

    test("should use fallback method when clipboard API not available", async () => {
      // Mock no Web Share API
      delete mockNavigator.share;
      delete mockNavigator.canShare;

      // Mock no clipboard API
      delete mockNavigator.clipboard;

      // Mock successful execCommand
      document.execCommand.mockReturnValue(true);

      const { result } = renderHook(() => useShare());
      const shareData = { url: "https://example.com" };

      await act(async () => {
        const shareResult = await result.current.shareContent(shareData);
        expect(shareResult).toEqual({ success: true, method: "fallback" });
      });

      expect(document.execCommand).toHaveBeenCalledWith("copy");
      expect(alert).toHaveBeenCalledWith("链接已复制到剪贴板！");
    });

    test("should use manual method when all else fails", async () => {
      // Mock no Web Share API
      delete mockNavigator.share;
      delete mockNavigator.canShare;

      // Mock no clipboard API
      delete mockNavigator.clipboard;

      // Mock failed execCommand
      document.execCommand.mockReturnValue(false);

      const { result } = renderHook(() => useShare());
      const shareData = { url: "https://example.com" };

      await act(async () => {
        const shareResult = await result.current.shareContent(shareData);
        expect(shareResult).toEqual({ success: false, method: "manual" });
      });

      expect(prompt).toHaveBeenCalledWith(
        "请手动复制以下链接:",
        "https://example.com",
      );
    });

    test("should handle clipboard writeText failure", async () => {
      mockNavigator.share.mockRejectedValue(new Error("Share cancelled"));
      mockNavigator.canShare.mockReturnValue(true);
      mockNavigator.clipboard.writeText.mockRejectedValue(
        new Error("Clipboard error"),
      );

      const { result } = renderHook(() => useShare());
      const shareData = { url: "https://example.com" };

      await act(async () => {
        const shareResult = await result.current.shareContent(shareData);
        expect(shareResult).toEqual({ success: false, method: "manual" });
      });

      expect(prompt).toHaveBeenCalledWith(
        "请手动复制以下链接:",
        "https://example.com",
      );
    });
  });
});

describe("share capability detection", () => {
  test("canUseWebShare should return true when Web Share API is available", () => {
    mockNavigator.share = jest.fn();
    mockNavigator.canShare = jest.fn();
    expect(canUseWebShare()).toBe(true);
  });

  test("canUseWebShare should return false when Web Share API is not available", () => {
    delete mockNavigator.share;
    delete mockNavigator.canShare;
    expect(canUseWebShare()).toBe(false);
  });

  test("canUseClipboard should return true when Clipboard API is available", () => {
    mockNavigator.clipboard = { writeText: jest.fn() };
    expect(canUseClipboard()).toBe(true);
  });

  test("canUseClipboard should return false when Clipboard API is not available", () => {
    delete mockNavigator.clipboard;
    expect(canUseClipboard()).toBe(false);
  });

  test("getShareCapabilities should return correct capabilities", () => {
    mockNavigator.share = jest.fn();
    mockNavigator.canShare = jest.fn();
    mockNavigator.clipboard = { writeText: jest.fn() };

    const capabilities = getShareCapabilities();
    expect(capabilities).toEqual({
      webShare: true,
      clipboard: true,
      fallback: true,
    });
  });

  test("getShareCapabilities should handle missing APIs", () => {
    delete mockNavigator.share;
    delete mockNavigator.canShare;
    delete mockNavigator.clipboard;

    const capabilities = getShareCapabilities();
    expect(capabilities).toEqual({
      webShare: false,
      clipboard: false,
      fallback: true,
    });
  });
});
