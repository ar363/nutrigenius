<script lang="ts">
	import { formatDistance } from 'date-fns';
	import { onMount } from 'svelte';

	let pastMeals = [];

	onMount(async () => {
		const res = await fetch('http://localhost:8000/cc/api/past-meals', {
			headers: {
				Authorization: `Bearer ${localStorage.getItem('token')}`
			}
		});
		const body = await res.json();
		pastMeals = body;
	});

	function relTime(dt: string) {
		return formatDistance(dt, new Date(), { addSuffix: true });
	}
</script>

<div class="mx-auto max-w-screen-xl p-4">
	<h1 class="text-2xl font-bold">Dashboard</h1>
	<div class="mt-4">
		<h2 class="text-xl">Past meals</h2>

		<table class="table border">
			<thead>
				<tr>
					<th>Food</th>
					<th>Quantity</th>
					<th>Calories</th>
					<th>Nutrients</th>
					<th>Time</th>
				</tr>
			</thead>
			<tbody>
				{#each pastMeals as meal}
					<tr>
						<td>{meal.food}</td>
						<td>{meal.quantity}</td>
						<td>{meal.calories}</td>
						<td>{meal.nutrients}</td>
						<td>{relTime(meal.created_at)}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
	<div class="mt-6 grid grid-cols-4 gap-4">
		<div class="card bg-base-100 w-full max-w-96 border shadow-xl">
			<div class="card-body">
				<h2 class="card-title">CalorieCraft AI</h2>
				<p>Track nutrition intake using images of your food</p>
				<div class="card-actions justify-start">
					<a class="btn btn-primary btn-sm mt-3" href="/cal">Go to page</a>
				</div>
			</div>
		</div>
		<div class="card bg-base-100 w-full max-w-96 border shadow-xl">
			<div class="card-body">
				<h2 class="card-title">PantryPilot AI</h2>
				<p>Check how much stock of food your refridgerator has</p>
				<div class="card-actions justify-start">
					<a class="btn btn-primary btn-sm mt-3" href="/cal">Go to page</a>
				</div>
			</div>
		</div>
	</div>
</div>
