SELECT

gameid,
CAST(REPLACE(starttime,'T',' ') AS TIMESTAMP) AS starttime,
CAST(REPLACE(endtime,'T',' ') AS TIMESTAMP) AS endtime,
hometrackingdata,
awaytrackingdata

FROM tracking_game_range

WHERE CAST(REPLACE(starttime,'T',' ') AS TIMESTAMP)=CAST('2020-02-03 02:51:13.399' AS TIMESTAMP) AND gameid='2020020200'