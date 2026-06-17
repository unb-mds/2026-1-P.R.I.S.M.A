tailwind.config = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#00152a',
          secondary: '#44617d',
          surface: '#f6fafe',
          'surface-container': '#ffffff',
          outline: '#c3c6ce',
          text: '#171c1f',
          'text-muted': '#43474d',
          success: '#00a472',
          warning: '#baba00',
          error: '#ba1a1a',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['IBM Plex Sans', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      }
    }
  }
}