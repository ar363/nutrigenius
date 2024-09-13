import type { Config } from 'tailwindcss';
import daisyui from 'daisyui';
import defaultTheme from 'tailwindcss/defaultTheme'

export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],

	theme: {
		extend: {
			fontFamily: {
				sans: ['Inter', ...defaultTheme.fontFamily.sans],
			}
		}
	},

	plugins: [
		daisyui,
	],

	daisyui: {
		themes: ['light']
	}
} as Config;
