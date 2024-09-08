<script lang="ts">
	let files: FileList;
	let result: object;
	let avatar;

	const formSubmit = async () => {
		const formData = new FormData();
		formData.append('file', files[0]);

		let reader = new FileReader();
		reader.readAsDataURL(files[0]);
		reader.onload = (e) => {
			avatar = e.target?.result;
		};

		try {
			const res = await fetch('http://localhost:8000/cc/api/predict-img', {
				method: 'POST',
				body: formData
			});
			const data = await res.json();
			result = data;
		} catch (error) {
			console.error(error);
		}
	};
</script>

<div class="mx-auto max-w-screen-xl p-4">
	<h1 class="text-2xl font-semibold">caloriecraft</h1>
	<form on:submit|preventDefault={formSubmit}>
		<div class="form-control">
			<div class="label">
				<label for="file" class="label-text">Upload image:</label>
			</div>
			<input type="file" bind:files name="file" id="file" class="file-input" />
		</div>
		<button type="submit" class="btn btn-primary mt-4">Submit</button>
	</form>

    {#if avatar}
        <div class="mt-4">
            <img src={avatar} alt="avatar" class="w-32 h-32 rounded-sm" />
        </div>
    {/if}

	{#if result}
		<div class="mt-4">
			<h2 class="text-xl font-semibold">Result:</h2>
			<pre>
                <code>
                    {JSON.stringify(result, null, 2)}
                </code>
            </pre>
		</div>
	{/if}
</div>
