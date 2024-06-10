/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      backgroundColor:{
        // Configure your background colors here
      },
      colors:{
        // Configure your color palette here
      },
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}

