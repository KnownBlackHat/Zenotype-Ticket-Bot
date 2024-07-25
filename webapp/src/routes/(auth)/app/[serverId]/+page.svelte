<script lang="ts">
	import { goto } from '$app/navigation';
	import type { Panel } from '$controllers/ipc';

	export let data: { data: Panel[] };
</script>

PANEL HERE
<button class="bg-blue-500" on:click={() => goto('create')}>
	PLACE A CREATE PANEL BUTTON HERE
</button>
{#each data.data as panel}
	{panel.title}
	{panel.description}
{/each}
