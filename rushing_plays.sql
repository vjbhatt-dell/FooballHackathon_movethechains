SELECT 
CAST(nfls.play_id AS INTEGER) AS play_id,
CAST(nfls.game_id AS INTEGER) AS game_id,
nfls.posteam,
nfls.defteam,
nfls.home_team,
nfls.away_team,
nfls.down,
nfls.game_seconds_remaining,
nfls.yardline_100,
nfls.ydstogo,
nfls.yards_gained,
nfls.score_differential,
nfls.rusher_player_id,
nfls.rusher_player_name,
nfls.run_location,
nfls.run_gap,
CAST(REPLACE(sp.starttime,'T',' ') AS TIMESTAMP) AS startplaytime,
CAST(REPLACE(sp.endtime,'T',' ') AS TIMESTAMP) AS endplaytime

FROM nflscrapr_data nfls 

LEFT JOIN tracking_game_range_playid sp ON sp.gameid=nfls.game_id AND sp.playid=CAST(nfls.play_id AS INTEGER)

WHERE nfls.rush_attempt='1' AND CAST(sp.gameid AS INTEGER)>2018000000 AND nfls.down IN ('1','2') AND CAST(nfls.game_seconds_remaining AS INTEGER)>120 AND nfls.game_id='2019010500'