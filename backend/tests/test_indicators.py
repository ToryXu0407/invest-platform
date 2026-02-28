/**
 * @vitest-environment jsdom
 */
import { describe, it, expect } from 'vitest';
import { indicator_calculator } from '@/services/indicator_calculator';

describe('核心指标计算器', () => {
  describe('股息率计算', () => {
    it('应该正确计算股息率', () => {
      const result = indicator_calculator.calculate_dividend_yield(25.91, 1678.50);
      expect(result).toBeCloseTo(1.54, 2);
    });

    it('股价为 0 时应该返回 null', () => {
      const result = indicator_calculator.calculate_dividend_yield(25.91, 0);
      expect(result).toBeNull();
    });
  });

  describe('PE-TTM 计算', () => {
    it('应该正确计算 PE-TTM', () => {
      const result = indicator_calculator.calculate_pe_ttm(
        2100000000000,
        [60000000000, 55000000000, 58000000000, 62000000000]
      );
      expect(result).toBeCloseTo(8.94, 2);
    });

    it('亏损时应该返回 null', () => {
      const result = indicator_calculator.calculate_pe_ttm(
        100000000000,
        [-1000000000, -2000000000, -1500000000, -1800000000]
      );
      expect(result).toBeNull();
    });
  });

  describe('真钱指数计算', () => {
    it('应该正确计算真钱指数', () => {
      const result = indicator_calculator.calculate_true_money_index(800, 700);
      expect(result).toBeCloseTo(1.14, 2);
    });

    it('净利润为 0 时应该返回 null', () => {
      const result = indicator_calculator.calculate_true_money_index(800, 0);
      expect(result).toBeNull();
    });

    it('真钱指数大于 1 表示利润质量优秀', () => {
      const result = indicator_calculator.calculate_true_money_index(800, 700);
      expect(result).toBeGreaterThan(1.0);
    });
  });

  describe('百分位计算', () => {
    it('应该正确计算百分位', () => {
      const historical = [20, 25, 30, 35, 40, 25, 28, 32, 38, 42];
      const result = indicator_calculator.calculate_percentile(28.5, historical);
      expect(result).toBe(40.0);
    });

    it('空数据应该返回 null', () => {
      const result = indicator_calculator.calculate_percentile(28.5, []);
      expect(result).toBeNull();
    });
  });

  describe('估值状态判断', () => {
    it('百分位<20% 应该是低估', () => {
      expect(indicator_calculator.get_valuation_status(15)).toBe('undervalued');
    });

    it('百分位 20-50% 应该是偏低', () => {
      expect(indicator_calculator.get_valuation_status(35)).toBe('low');
    });

    it('百分位 50-80% 应该是合理', () => {
      expect(indicator_calculator.get_valuation_status(60)).toBe('fair');
    });

    it('百分位 80-90% 应该是偏高', () => {
      expect(indicator_calculator.get_valuation_status(85)).toBe('high');
    });

    it('百分位>90% 应该是高估', () => {
      expect(indicator_calculator.get_valuation_status(95)).toBe('overvalued');
    });
  });
});
