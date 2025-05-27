<template>
  <svg
    width="20"
    height="20"
    viewBox="0 0 20 20"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
  >
    <rect width="20" height="20" fill="url(#pattern0_28_176)" />
    <defs>
      <pattern
        id="pattern0_28_176"
        patternContentUnits="objectBoundingBox"
        width="1"
        height="1"
      >
        <use xlink:href="#image0_28_176" transform="scale(0.0111111)" />
      </pattern>
      <image
        id="image0_28_176"
        width="90"
        height="90"
        xlink:href="data:image/png;base64,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"
      />
    </defs>
  </svg>
</template>
