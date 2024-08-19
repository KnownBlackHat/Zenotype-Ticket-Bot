<script lang="ts">
	import type { ActionData } from './$types';

	export let form: ActionData;
	interface FormFields {
		display: string;
		name: string;
		required?: boolean;
		type?: string;
	}
	let obj: Record<string, FormFields[]> = {
		Panel_Message: [
			{ display: 'Title', name: 'title', required: true },
			{ display: 'Description', name: 'description' },
			{ display: 'Color', name: 'color' },
			{ display: 'Channel', name: 'channel', type: 'number' },
			{ display: 'Disable Panel', name: 'disable_panel', type: 'checkbox' }
		],
		Panel_Button: [
			{ display: 'Button Color', name: 'button_color' },
			{ display: 'Button Text', name: 'button_text' },
			{ display: 'Button Emoji', name: 'button_emoji' }
		],
		Ticket_Properties: [
			{ display: 'Mention On Open', name: 'mention_on_open' },
			{ display: 'Support Team', name: 'support_team' },
			{ display: 'Category', name: 'category' },
			{ display: 'Naming Scheme', name: 'naming_scheme' }
		],
		Images: [
			{ display: 'Large Image Url (Optional)', name: 'large_image(optional)' },
			{ display: 'Small Image Url (Optional)', name: 'small_image(optional)' }
		],
		Welcome_Message: [
			{ display: 'Title (Optional)', name: 'wlcm_title(optional)' },
			{ display: 'Description (Optional)', name: 'wlcm_description(optional)' },
			{ display: 'Color (Optional)', name: 'wlcm_color(optional)' }
		],
		Author: [
			{ display: 'Name', name: 'author_name' },
			{ display: 'Icon Url (Optional)', name: 'author_url(optional)' }
		],
		Access_Control: [{ display: 'Roles', name: 'roles' }]
	};
</script>

<div class="flex">
	<div class="container mx-auto p-4 pt-6 md:p-6 lg:p-12">
		{#if form?.success === false}
			<div class="bg-red-600 rounded-md p-2 m-2 text-center font-bold">Error: {form?.error}</div>
		{:else if form?.success === true}
			<div class="bg-green-600 rounded-md p-2 m-2 text-center font-bold">
				Panel Created Successfully!
			</div>
		{/if}
		<form method="POST" action="?/panelSubmit">
			<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
				{#each Object.entries(obj) as [key, ent]}
					<div id="embed" class="bg-black p-4 border-2 border-white rounded-lg shadow-md">
						<h2 class="text-lg font-bold text-white mb-4">{key.replace('_', ' ')}</h2>
						{#each ent as { display, name, required, type }}
							<div class="flex-col mb-4" class:flex={!(type === 'checkbox')}>
								<label class="text-sm text-gray-400" for={name}>{display}:</label>
								<input
									type={type ?? 'text'}
									inputmode={type === 'number' ? 'numeric' : null}
									{name}
									class="rounded-md p-2 bg-gray-200 text-black focus:bg-white focus:outline-none"
									{required}
								/>
							</div>
						{/each}
					</div>
				{/each}
			</div>
			<div class="text-center m-2">
				<button type="submit" class="p-2 bg-blue-600 rounded-md">Submit</button>
			</div>
		</form>
	</div>
</div>
