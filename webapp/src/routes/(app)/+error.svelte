<script>
	import { page } from '$app/stores';
</script>

<div class="flex items-center justify-center h-screen">
	<div class="bg-black text-2xl font-bold py-40 px-48 rounded-lg">
		{#if $page.status == 403}
			You are not authorized to access this page
		{:else if $page.status == 404}
			The page you are looking for does not exist
		{:else if $page.status == 500}
			An error occurred while processing your request
		{:else}
			Something went wrong (Error code: {$page.status})
		{/if}
	</div>
</div>
