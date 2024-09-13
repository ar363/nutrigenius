<script lang="ts">
	import { goto } from '$app/navigation';
	import { getUserToken } from '$lib/frontendUtils';

	let files: FileList;
	let result: object;
	let avatar;
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

			for (let dx of data.op) {
			}
		} catch (error) {
			console.error(error);
		}
	};

	const addFoodToDiet = async () => {
		const formData = new FormData(document.querySelector('#add_food_form'));

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

			{#if avatar}
				<div class="mt-4">
					<img src={avatar} alt="avatar" class="h-full w-full rounded-md" />
				</div>
			{/if}

			{#if result}
				<div role="tablist" class="tabs tabs-boxed mt-6 max-w-xs">
					<button
						role="tab"
						class={`tab ${activeTab == 'IN' ? 'tab-active' : ''}`}
						on:click={() => {
							activeTab = 'IN';
							tabViewMore = false;
						}}>FSSAI Model</button
					>
					<button
						role="tab"
						class={`tab ${activeTab == 'US' ? 'tab-active' : ''}`}
						on:click={() => {
							activeTab = 'US';
							tabViewMore = false;
						}}>FDA Model</button
					>
				</div>

				{#if activeTab == 'IN'}
					<div class="card bg-base-100 mt-4 w-full max-w-96 border shadow-lg">
						<div class="card-body">
							<h2 class="card-title">{result.ind[0].name}</h2>
							<p>Confidence: {round2(result.ind[0].confidence)}</p>
							<div class="card-actions justify-start">
								<button
									class="btn btn-primary btn-sm"
									on:click={() => setSelectedFood(result.ind[0].name)}>Next &rarr;</button
								>
							</div>
						</div>
					</div>

					{#if tabViewMore}
						<div class="card bg-base-100 mt-4 w-full max-w-96 border shadow-lg">
							<div class="card-body">
								<h2 class="card-title">{result.ind[1].name}</h2>
								<p>Confidence: {round2(result.ind[1].confidence)}</p>
								<div class="card-actions justify-start">
									<button
										class="btn btn-primary btn-sm"
										on:click={() => setSelectedFood(result.ind[1].name)}>Next &rarr;</button
									>
								</div>
							</div>
						</div>

						<div class="card bg-base-100 mt-4 w-full max-w-96 border shadow-lg">
							<div class="card-body">
								<h2 class="card-title">{result.ind[2].name}</h2>
								<p>Confidence: {round2(result.ind[2].confidence)}</p>
								<div class="card-actions justify-start">
									<button
										class="btn btn-primary btn-sm"
										on:click={() => setSelectedFood(result.ind[2].name)}>Next &rarr;</button
									>
								</div>
							</div>
						</div>
					{:else}
						<button
							type="button"
							class="btn btn-sm mt-6"
							on:click={() => {
								tabViewMore = true;
							}}>View More</button
						>
					{/if}
				{:else}<div class="card bg-base-100 mt-4 w-full max-w-96 border shadow-lg">
						<div class="card-body">
							<h2 class="card-title">{result.us[0].name}</h2>
							<p>Confidence: {round2(result.us[0].confidence)}</p>
							<div class="card-actions justify-start">
								<button
									class="btn btn-primary btn-sm"
									on:click={() => setSelectedFood(result.us[0].name)}>Next &rarr;</button
								>
							</div>
						</div>
					</div>

					{#if tabViewMore}
						<div class="card bg-base-100 mt-4 w-full max-w-96 border shadow-lg">
							<div class="card-body">
								<h2 class="card-title">{result.us[1].name}</h2>
								<p>Confidence: {round2(result.us[1].confidence)}</p>
								<div class="card-actions justify-start">
									<button
										class="btn btn-primary btn-sm"
										on:click={() => setSelectedFood(result.us[1].name)}>Next &rarr;</button
									>
								</div>
							</div>
						</div>

						<div class="card bg-base-100 mt-4 w-full max-w-96 border shadow-lg">
							<div class="card-body">
								<h2 class="card-title">{result.us[2].name}</h2>
								<p>Confidence: {round2(result.us[2].confidence)}</p>
								<div class="card-actions justify-start">
									<button
										class="btn btn-primary btn-sm"
										on:click={() => setSelectedFood(result.us[2].name)}>Next &rarr;</button
									>
								</div>
							</div>
						</div>
					{:else}
						<button
							class="btn btn-sm mt-6"
							type="button"
							on:click={() => {
								tabViewMore = true;
							}}>View More</button
						>
					{/if}
				{/if}
			{/if}
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
