<script lang="ts">
	import { onMount } from 'svelte';
	import SvelteMarkdown from 'svelte-markdown';

	let suggestion = '';

	onMount(async () => {
		await fetch('http://localhost:8000/cc/api/recipegen', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${localStorage.getItem('token')}`
			}
		})
			.then((res) => res.json())
			.then((data) => {
				suggestion = data.message;
			})
			.catch((error) => {
				console.error(error);
			});
	});
</script>

<div class="mx-auto max-w-screen-xl p-4">
	<h1 class="text-2xl font-bold mb-6">RecipeRevolution suggestion:</h1>

	<SvelteMarkdown source={suggestion} />
</div>
