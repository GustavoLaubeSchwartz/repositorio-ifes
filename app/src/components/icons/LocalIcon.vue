<template>
  <svg
    width="20"
    height="20"
    viewBox="0 0 20 20"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
  >
    <rect width="20" height="20" fill="url(#pattern0_25_44)" />
    <defs>
      <pattern
        id="pattern0_25_44"
        patternContentUnits="objectBoundingBox"
        width="1"
        height="1"
      >
        <use xlink:href="#image0_25_44" transform="scale(0.0111111)" />
      </pattern>
      <image
        id="image0_25_44"
        width="90"
        height="90"
        xlink:href="data:image/png;base64,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"
      />
    </defs>
  </svg>
</template>
