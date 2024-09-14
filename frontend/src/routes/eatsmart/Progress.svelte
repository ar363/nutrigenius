<script>
	import { onMount } from 'svelte';

	export let progress = 0;
	export let colorClass = 'bg-blue-600';
</script>

<div style="background-color: #bbb; max-width: 400px; margin-bottom: 16px;">
	<div
		style={'height: 4px; border-radius: 8px; width: ' +
			(progress * 100) +
			'%; background-color: rgb(' +
			colorClass +
			')'}
	></div>
</div>
