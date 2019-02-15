//MINING-1 // CLUSTER
/obj/effect/overmap/sector/pleasure
	name = "Bluespace Rift"
	desc = "A strange Bluespace Rift. Standing orders dictate exploration is a high priority."
	icon_state = "sector"
	initial_generic_waypoints = list(
		"nav_pleasure_1"
	)
	known = 1
	start_x = 6
	start_y = 5

/datum/map_template/ruin/away_site/pleasure
	name = "Pleasure Planet"
	id = "awaysite_pleasure"
	description = "A pleasure planet"
	suffixes = list("pleasure/beach.dmm")
	cost = 0
	accessibility_weight = 10
	template_flags = TEMPLATE_FLAG_SPAWN_GUARANTEED


/datum/map_template/ruin/away_site/pleasure/init_atoms(var/list/atoms)
	. = ..(atoms)

	for (var/atom/A in atoms)
		if (istype(A, /turf))
			var/turf/T = A
			T.set_light(1, 0.5, 2)

/obj/effect/shuttle_landmark/pleasure/nav1
	name = "Enter Bluespace Rift"
	landmark_tag = "nav_pleasure_1"

/area/beach/planet
	name = "Pleasure Planet beach"
	luminosity = 1
	dynamic_lighting = 1
	requires_power = 0
	area_flags = AREA_FLAG_RAD_SHIELDED | AREA_FLAG_ION_SHIELDED | AREA_FLAG_IS_NOT_PERSISTENT
	base_turf = ...
	var/annoy = FALSE
	var/annoy_vol = 100

/area/beach/planet/process()
	set background = 1

	if (annoy)
		var/sound/S = null
		var/sound_delay = 0
		if(prob(25))
			S = sound(file=pick('sound/ambience/seag1.ogg','sound/ambience/seag2.ogg','sound/ambience/seag3.ogg'), volume=annoy_vol)
			sound_delay = rand(0, 50)

		for(var/mob/living/carbon/human/H in src)
			if(H.client)
				mysound.status = SOUND_UPDATE
				to_chat(H, mysound)
				if(S)
					spawn(sound_delay)
						sound_to(H, S)

	spawn(60) .()


/area/beach/planet/interior
	name = "Pleasure Planet inside"
	annoy_vol = 33