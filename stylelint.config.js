module.exports = {
  extends: ["stylelint-config-suitcss", "stylelint-config-prettier"],
  plugins: ["stylelint-selector-bem-pattern"],
  rules: {
    "rule-empty-line-before": null,
    "plugin/selector-bem-pattern": {
      preset: "suit",
      componentName: "[A-Z]+",
      componentSelectors: {
        initial:
          "^\\.{componentName}(?:-[a-zA-Z0-9]+)?(?:--[a-zA-Z0-9]+)?(?:.is-[a-zA-Z0-9]+)?$",
      },
      utilitySelectors: "^\\.u-[a-zA-Z0-9]+$",
    },
  },
};
