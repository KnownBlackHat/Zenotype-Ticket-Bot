<script lang="ts">
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
			{ display: 'Large Image Url', name: 'large_image_url' },
			{ display: 'Small Image Url', name: 'small_image_url' }
		],
		Welcome_Message: [
			{ display: 'Title', name: 'wlcm_title' },
			{ display: 'Description', name: 'wlcm_description' },
			{ display: 'Color', name: 'wlcm_color' }
		],
		Author: [
			{ display: 'Name', name: 'author_name' },
			{ display: 'Icon Url (Optional)', name: 'author_icon_url' }
		],
		Access_Control: [{ display: 'Roles', name: 'roles' }]
	};
</script>

<div class="flex">
	<div class="container mx-auto p-4 pt-6 md:p-6 lg:p-12">
		<form method="POST">
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
