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
	<h1 class="text-2xl font-bold">
		<img src="/nutrigeniuslogo.png" alt="" class="-ml-[20px] w-[450px]" />
	</h1>
	<div class="mt-4">
		<h2 class="text-xl">Past meals</h2>

		<table class="table border">
			<thead>
				<tr>
					<th>Food</th>
					<th>Quantity</th>
					<th>Calories</th>
					<th>Protein</th>
					<th>Fat</th>
					<th>Carbs</th>
					<th>Sodium</th>
					<th>Time</th>
				</tr>
			</thead>
			<tbody>
				{#each pastMeals as meal}
					<tr>
						<td>{meal.food}</td>
						<td>{meal.quantity}</td>
						<td>{meal.food_data.calories}</td>
						<td>{meal.food_data.protein}g</td>
						<td>{meal.food_data.fat}g</td>
						<td>{meal.food_data.carbs}g</td>
						<td class={meal.food_data.sodium > 100 ? 'text-red-700' : ''}
							>{meal.food_data.sodium}mg</td
						>
						<td>{relTime(meal.created_at)}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
	<div class="mt-6 grid grid-cols-4 gap-4">
		<a href="/cal">
			<div class="card w-full max-w-96 border bg-purple-200 shadow-xl">
				<div class="card-body">
					<h2 class="card-title">CalorieCraft AI</h2>
					<p>Track nutrition intake using images of your food</p>
				</div>
			</div>
		</a>
		<a href="/pantry">
			<div class="card w-full max-w-96 border bg-pink-100 shadow-xl">
				<div class="card-body">
					<h2 class="card-title">PantryPilot AI</h2>
					<p>Check how much stock of food your refridgerator has</p>
				</div>
			</div>
		</a>
	</div>
</div>
