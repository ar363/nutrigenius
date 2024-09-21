<script lang="ts">
	import { goto } from '$app/navigation';
	import { getUserToken, setUserToken } from '$lib/frontendUtils';

	let signupError = '';

	function submitSignupForm() {
		//@ts-ignore
		const fd = new FormData(document.querySelector('#register_modal form'));
		const json = Object.fromEntries(fd.entries());

		fetch('http://localhost:8000/cc/api/signup', {
			method: 'POST',
			body: JSON.stringify(json),
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include'
		})
			.then((res) => res.json())
			.then((data) => {
				if (data.error) {
					signupError = data.error;
					return;
				}
				setUserToken(data.token);
				goto('/dashboard');
			})
			.catch((err) => {
				console.error(err);
			});
	}
</script>

<div class="min-h-screen bg-gradient-to-b from-green-50 to-blue-50">
	<header class="container mx-auto flex items-center justify-between px-4 py-6">
		<div class="flex items-center space-x-2">
			<span class="text-2xl font-bold text-gray-800 max-w-[220px]">
				<img src="/nutrigeniuslogo.png" alt="">
			</span>
		</div>
		<nav>
			<ul class="flex space-x-4">
				<!-- <li><a data-sveltekit-reload href="#" class="text-gray-600 hover:text-gray-800">Home</a></li>
				<li><a data-sveltekit-reload href="#" class="text-gray-600 hover:text-gray-800">About</a></li>
				<li><a data-sveltekit-reload href="#" class="text-gray-600 hover:text-gray-800">Contact</a></li> -->
			</ul>
		</nav>
	</header>
	<main class="container mx-auto flex flex-col items-center px-4 py-12 lg:flex-row">
		<div class="lg:w-1/2 lg:pr-12">
			<h1 class="mb-4 text-4xl font-bold text-gray-800 lg:text-5xl">
				Your Personal AI Nutritionist
			</h1>
			<p class="mb-8 text-xl text-gray-600">
				Get personalized meal plans, nutrition advice, and health insights powered by artificial
				intelligence.
			</p>
			{#if !getUserToken()}
				<button
					on:click={() => {
						//@ts-ignore
						document.getElementById('register_modal').showModal();
					}}
					class="rounded-lg bg-green-600 px-6 py-3 text-lg font-bold text-white hover:bg-green-700"
				>
					Sign Up Now
				</button>
			{:else}
				<a data-sveltekit-reload
					href="/dashboard"
					class="rounded-lg bg-green-600 px-6 py-3 text-lg font-bold text-white hover:bg-green-700"
					>Go to dashboard</a
				>
			{/if}
		</div>
		<div class="mt-12 lg:mt-0 lg:w-1/2">
			<img src="/land.png" alt="AI Nutritionist Illustration" class="mx-auto w-full max-w-sm" />
		</div>
	</main>
</div>

<dialog id="register_modal" class="modal">
	<div class="modal-box max-w-sm">
		<form method="post" on:submit|preventDefault={submitSignupForm}>
			<h3 class="text-lg font-bold">Signup / Login</h3>
			{#if signupError}
				<p class="text-red-500">{signupError}</p>
			{/if}
			<input
				type="email"
				placeholder="Your Email"
				name="email"
				class="input input-bordered mt-4 w-full"
				required
			/>
			<input
				type="password"
				placeholder="Your Password"
				name="password"
				class="input input-bordered mt-4 w-full"
				minlength="4"
			/>
			<button class="btn btn-primary mt-4 w-full text-lg" type="submit">Signup / Login</button>
		</form>
	</div>
	<form method="dialog" class="modal-backdrop">
		<button>close</button>
	</form>
</dialog>
