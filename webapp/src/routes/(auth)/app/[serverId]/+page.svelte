<script lang="ts">
	import { goto } from '$app/navigation';
	import type { Panel } from '$controllers/ipc';

	export let data: { data: Panel[] };
</script>

PANEL HERE
<button class="bg-blue-500" on:click={() => goto('create')}>
	PLACE A CREATE PANEL BUTTON HERE
</button>
{#if data.data.length === 0}
	<div class="flex items-center justify-center h-screen">
		<div class="bg-black text-2xl font-bold py-40 px-48 rounded-lg">
			No panels configured for this server
		</div>
	</div>
{:else}
	<div class="grid md:grid-cols-5 md:gap-5 mx-2">
		{#each data.data as panel}
			{panel.title}
			{panel.description}
		{/each}
	</div>
{/if}
