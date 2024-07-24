CREATE TABLE poker.win_rates (
	card_1_rank int8 NULL,
	card_2_rank int8 NULL,
	suited bool NULL,
	wins float8 NULL,
	counts float8 NULL,
	win_rate float8 NULL,
	"rank" int8 NULL,
	percentile float8 NULL,
	player_count int8 NULL,
	sklansky int8 NULL,
	sklansky_position text NULL,
	modified_sklansky int8 NULL,
	modified_sklansky_position text NULL
);