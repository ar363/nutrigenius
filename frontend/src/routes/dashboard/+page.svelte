<script lang="ts">
	import { onMount } from 'svelte';
	import { Doughnut } from 'svelte-chartjs';
	import { formatDistance } from 'date-fns';
	import 'chart.js/auto'; // Ensure you import this to auto-register all components

	let pastMeals = [];
	let sums = {
		protein: 0,
		fat: 0,
		carbs: 0,
		calories: 0
	};
	const dailyNutrientGoals = {
		protein: 60,
		fat: 55,
		carbs: 275,
		calories: 2400
	};

	onMount(async () => {
		const res = await fetch('http://localhost:8000/cc/api/past-meals', {
			headers: {
				Authorization: `Bearer ${localStorage.getItem('token')}`
			}
		});
		const body = await res.json();
		pastMeals = body.meals;
		sums = body.sums;
	});

	function relTime(dt: string) {
		return formatDistance(new Date(dt), new Date(), { addSuffix: true });
	}

	function calcData(mealdata: any) {
		return {
			labels: ['Protein', 'Fat', 'Carbs'],
			datasets: [
				{
					data: [mealdata.protein, mealdata.fat, mealdata.carbs],
					backgroundColor: ['#009EDB', '#f50', '#008037'],
					hoverBackgroundColor: ['#009EDB', '#f50', '#008037']
				}
			]
		};
	}
</script>

<div class="mx-auto max-w-screen-xl p-4">
	<h1 class="text-2xl font-bold">
		<img src="/nutrigeniuslogo.png" alt="" class="-ml-[20px] w-[450px]" />
	</h1>
	<div class="mt-4">
		<div class="mb-5 mt-6 grid gap-4 md:grid-cols-4">
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
			<a href="/eatsmart">
				<div class="card w-full max-w-96 border bg-lime-100 shadow-xl">
					<div class="card-body">
						<h2 class="card-title">EatSmart Dietician</h2>
						<p>AI powered dietician based on realtime data</p>
					</div>
				</div>
			</a>
			<a href="/reciperevolution">
				<div class="card w-full max-w-96 border bg-amber-100 shadow-xl">
					<div class="card-body">
						<h2 class="card-title">RecipeRevolution AI</h2>
						<p>AI powered dietician based on realtime data</p>
					</div>
				</div>
			</a>
		</div>

		<h2 class="mt-6 mb-4 text-lg">Today's Nutrition</h2>


		<div class="flex items-center gap-8">
			<div class="flex flex-col items-center">
				<div
					class="radial-progress text-primary"
					style={`--value:${(100 * sums.protein) / dailyNutrientGoals.protein};`}
					role="progressbar"
				>
					{Math.round((100 * sums.protein) / dailyNutrientGoals.protein)}%
				</div>
				<div class="text-primary">Protien</div>
			</div>
			<div class="flex flex-col items-center">
				<div
					class="radial-progress text-purple-700"
					style={`--value:${(100 * sums.fat) / dailyNutrientGoals.fat};`}
					role="progressbar"
				>
					{Math.round((100 * sums.fat) / dailyNutrientGoals.fat)}%
				</div>
				<div class="text-purple-700">Fat</div>
			</div>
			<div class="flex flex-col items-center">
				<div
					class="radial-progress text-green-700"
					style={`--value:${(100 * sums.carbs) / dailyNutrientGoals.carbs};`}
					role="progressbar"
				>
					{Math.round((100 * sums.carbs) / dailyNutrientGoals.carbs)}%
				</div>
				<div class="text-green-700">Carbs</div>
			</div>
			<div class="flex flex-col items-center">
				<div
					class="radial-progress text-orange-600"
					style={`--value:${(100 * sums.calories) / dailyNutrientGoals.calories};`}
					role="progressbar"
				>
					{Math.round((100 * sums.calories) / dailyNutrientGoals.calories)}%
				</div>
				<div class="text-orange-600">Calories</div>
			</div>
		</div>

		<h2 class="mt-4 text-lg">Past meals</h2>

		<div class="mt-5 grid gap-4 md:grid-cols-4">
			{#each pastMeals as meal}
				<div class="card border">
					<div class="card-body">
						<h2 class="card-title">{meal.food}</h2>
						<p class="-mt-1 text-xs text-gray-600">{relTime(meal.created_at)}</p>
						<div class="w-[200px]">
							<Doughnut data={calcData(meal.food_data)} />
						</div>
						<ul class="ml-4 mt-2 list-disc">
							<li>{meal.food_data.calories} calories</li>
							<li>{meal.food_data.protein}g Protein</li>
							<li>{meal.food_data.fat}g Fat</li>
							<li>{meal.food_data.carbs}g Carbs</li>
							<li class={meal.food_data.sodium > 100 ? 'text-red-700' : ''}>
								{meal.food_data.sodium}mg Sodium
							</li>
							{#if meal.food_data.vitamins}
								<li class="text-emerald-600">Rich in Vitamin {meal.food_data.vitamins}</li>
							{/if}
							{#if meal.food_data.fiber && meal.food_data.fiber > 2}
								<li>{meal.food_data.fiber}g Fiber</li>
							{:else}
								<li class="text-red-700">Very low fiber</li>
							{/if}
						</ul>
					</div>
				</div>
			{/each}
		</div>
	</div>
</div>
