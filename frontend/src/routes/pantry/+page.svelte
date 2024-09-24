<script lang="ts">
	import { goto } from '$app/navigation';
	import { getUserToken } from '$lib/frontendUtils';

	let files: FileList;
	let result: { name: string; count: number }[];
	let avatar: string;
	let activeTab: 'IN' | 'US' = 'IN';
	let tabViewMore = false;
	let selectedFood: string;

	const formSubmit = async () => {
		const formData = new FormData();
		formData.append('image', files[0]);

		try {
			const res = await fetch('http://localhost:7001/yolo5', {
				method: 'POST',
				body: formData
			});
			const data = await res.json();
			avatar = data.img.slice(15);

			let fres = [];
			for (let dx of data.op) {
				if (fres.map((x) => x.name).includes(dx.name)) {
					let idx = fres.map((x) => x.name).indexOf(dx['name']);
					fres[idx]['count'] += 1;
				} else {
					fres.push({
						name: dx.name,
						count: 1
					});
				}
			}
			result = fres;
		} catch (error) {
			console.error(error);
		}
	};

	const addToPantry = async () => {
		fetch('http://localhost:8000/cc/api/add-pantry', {
			method: 'POST',
			body: JSON.stringify(result),
			headers: {
				Authorization: `Bearer ${getUserToken()}`,
				'Content-Type': 'application/json'
			}
		})
			.then((res) => res.json())
			.then((data) => {
				console.log(data);
				goto('/dashboard');
			})
			.catch((error) => {
				console.error(error);
			});
	};

	const addFoodToDiet = async () => {
		const formData = new FormData(document.querySelector('#add_food_form') as HTMLFormElement);

		try {
			const res = await fetch('http://localhost:8000/cc/api/add-food', {
				method: 'POST',
				body: JSON.stringify(Object.fromEntries(formData.entries())),
				headers: {
					Authorization: `Bearer ${getUserToken()}`,
					'Content-Type': 'application/json'
				}
			});
			const data = await res.json();

			goto('/dashboard');

			console.log(data);
		} catch (error) {
			console.error(error);
		}
	};

	function round2(num: number) {
		return Math.round(num * 100) / 100;
	}

	function setSelectedFood(food: string) {
		selectedFood = food;
	}
</script>

<div class="min-h-screen bg-pink-100">
	<div class="mx-auto max-w-screen-xl p-4">
		<h1 class="mb-6 text-xl font-semibold">PantryPilot AI</h1>
		{#if !selectedFood}
			<form on:submit|preventDefault={formSubmit} class="flex items-end gap-4">
				<div class="form-control">
					<div class="label">
						<label for="file" class="label-text">Upload or take photo of an image:</label>
					</div>
					<input
						type="file"
						bind:files
						name="image"
						id="file"
						class="file-input file-input-bordered max-w-72"
					/>
				</div>
				<button type="submit" class="btn btn-accent mt-4">What is in this pantry?</button>
			</form>

			<div class="flex gap-4">
				{#if avatar}
					<div class="mt-4">
						<img src={avatar} alt="avatar" class="h-full w-full rounded-md" />
					</div>
				{/if}

				{#if result}
					<form on:submit|preventDefault={addToPantry}>
						<div class="mt-4 grid w-full grid-cols-3 gap-4">
							{#each result as food}
								<div class="card bg-pink-50">
									<div class="card-body">
										<h2 class="card-title">{food.name}</h2>
										<label class="label" for={`fc__${food.name}`}>Count:</label>
										<input
											type="number"
											bind:value={food.count}
											id={`fc__${food.name}`}
											class="input input-bordered"
										/>
									</div>
								</div>
							{/each}
						</div>
						<button type="submit" class="btn btn-primary mt-4">Add to pantry</button>
					</form>
				{/if}
			</div>
		{:else}
			<h2 class="mt-4 text-2xl font-bold">{selectedFood}</h2>
			<p>???</p>
			<form method="post" on:submit|preventDefault={addFoodToDiet} id="add_food_form">
				<input type="hidden" name="sel_food" value={selectedFood} />
				<input
					type="number"
					class="input input-bordered"
					placeholder="Qty eaten"
					name="qty"
					id="qty"
					required
				/>
				<button type="submit" class="btn btn-accent mt-4">Add</button>
			</form>
		{/if}
	</div>
</div>
