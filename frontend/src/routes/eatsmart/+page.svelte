<script lang="ts">
	import { onMount } from 'svelte';
	import Progress from './Progress.svelte';
	import SvelteMarkdown from 'svelte-markdown';

	let weight = 70;
	let goal = '';
	let activity_level = '';
	let suggestion = '';

	let subdata = {
		weight: 70,
		goal: '',
		activity_level: ''
	};

	let reqdata: {
		min_calories: number;
		max_calories: number;
		min_fat: number;
		max_fat: number;
		min_protein: number;
		max_protein: number;
		min_carbs: number;
		max_carbs: number;
	} | null = null;

	onMount(async () => {
		await fetch('http://localhost:8000/cc/api/dietician', {
			method: 'POST',
			body: JSON.stringify(subdata),
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

	const handleSubmit = async () => {
		const formData = {
			weight: Number.parseInt(weight),
			goal,
			activity_level
		};

		try {
			const res = await fetch('http://localhost:8000/cc/api/fitness-tool', {
				method: 'POST',
				body: JSON.stringify(formData),
				headers: {
					'Content-Type': 'application/json'
				}
			});
			const data = await res.json();

			const j = giveJudgement(data);
			//@ts-ignore
			reqdata = data;
			subdata = formData;

			console.log(data);
		} catch (error) {
			console.error(error);
		}
	};

	const giveJudgement = (indata: {
		min_calories: number;
		max_calories: number;
		min_fat: number;
		max_fat: number;
		min_protein: number;
		max_protein: number;
		min_carbs: number;
		max_carbs: number;
	}) => {
		return {
			text: 'hhh'
		};
	};
</script>

<div class="mx-auto max-w-screen-xl p-4">
	<h1 class="text-2xl font-bold">EatSmart Dietician</h1>

	<SvelteMarkdown source={suggestion} />

	<p>Please answer the following questions to get a personalised diet recommendation</p>
	<form method="post" on:submit|preventDefault={handleSubmit}>
		<input
			type="number"
			name="weight"
			id="weight"
			class="input input-bordered mb-4 mt-6 w-[250px]"
			placeholder="Weight"
			bind:value={weight}
		/>

		<div class="form-control">
			<label for="goal" class="label">Goal</label>
			<select
				name="goal"
				id="goal"
				bind:value={goal}
				class="mb-4 bg-gray-50 px-4 py-3"
				style="background-color: white; border: 1px solid #ddd; border-radius: 8px; width: 250px"
			>
				<option value="weight_loss">Lose weight</option>
				<option value="maintenance">Maintain weight</option>
				<option value="weight_gain">Gain weight</option>
			</select>
		</div>

		<div class="form-control">
			<label for="activity_level" class="label">Lifestyle</label>

			<select
				name="activity_level"
				bind:value={activity_level}
				id="activity_level"
				class="mb-4 bg-gray-50 px-4 py-3"
				style="background-color: white; border: 1px solid #ddd; border-radius: 8px; width: 250px"
			>
				<option value="sedentary">Sedentary</option>
				<option value="moderate">Moderate</option>
				<option value="very_active">Very active</option>
			</select>
		</div>

		<button type="submit" class="btn btn-primary">Submit</button>
	</form>

	{#if reqdata}
		<div>
			<h2 class="mt-6 text-xl font-bold">Diet Recommendation</h2>

			<p>{reqdata.min_calories} - {reqdata.max_calories} calories</p>
			<Progress progress={reqdata.min_calories / reqdata.max_calories} colorClass="74,0,255" />

			<p>{reqdata.min_fat} - {reqdata.max_fat} grams of fat</p>
			<Progress progress={reqdata.min_fat / reqdata.max_fat} colorClass="255,0,211" />

			<p>{reqdata.min_protein} - {reqdata.max_protein} grams of protein</p>
			<Progress progress={reqdata.min_protein / reqdata.max_protein} colorClass="1,210,188" />

			<p>{reqdata.min_carbs} - {reqdata.max_carbs} grams of carbs</p>
			<Progress progress={reqdata.min_carbs / reqdata.max_carbs} colorClass="255,190,0" />
		</div>
	{/if}
</div>
