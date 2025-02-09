DROP TRIGGER IF EXISTS match_overlap;
DROP TRIGGER IF EXISTS coach_overlap;
DROP TRIGGER IF EXISTS player_overlap;
DELIMITER //

CREATE TRIGGER match_overlap BEFORE INSERT ON MatchSession
FOR EACH ROW
BEGIN
    DECLARE time_overlap INT;

    SELECT COUNT(*) INTO time_overlap
    FROM MatchSession M
    WHERE (M.stadium_ID = NEW.stadium_ID)
    AND M.match_date = NEW.match_date
    AND ((M.time_slot -1 <= NEW.time_slot) AND (NEW.time_slot <= M.time_slot + 1) );

    IF time_overlap > 0 THEN 
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'There already exists a match that occupies that time slot.';
    END IF;
END;
//

CREATE TRIGGER player_overlap BEFORE INSERT ON SessionSquads
FOR EACH ROW
BEGIN
    DECLARE time_overlap INT;

    SELECT COUNT(*) INTO time_overlap
    FROM 
    (SELECT M1.time_slot , M1.match_date FROM MatchSession M1, 
    (SELECT S1.session_ID as session_ID FROM SessionSquads S1 WHERE S1.played_player_username = NEW.played_player_username) Q1
    WHERE Q1.session_ID = M1.session_ID) Q, (SELECT M2.time_slot, M2.match_date FROM MatchSession M2 WHERE M2.session_ID = NEW.session_ID) M3
    WHERE  (Q.match_date = M3.match_date) AND ((Q.time_slot -1 <= M3.time_slot) AND (M3.time_slot <= Q.time_slot + 1));

    IF time_overlap > 0 THEN 
        SET @error_message = CONCAT('Player ', NEW.played_player_username, " plays another match in given time slot.");
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = @error_message;
    END IF;
END;
//

CREATE TRIGGER coach_overlap BEFORE INSERT ON Team
FOR EACH ROW
BEGIN
    DECLARE coach_overlap INT;

    SELECT COUNT(*) INTO coach_overlap
    FROM Team T
    WHERE (T.coach_username = NEW.coach_username)
    AND (((STR_TO_DATE(T.contract_start, '%d.%m.%Y') <= STR_TO_DATE(NEW.contract_start, '%d.%m.%Y')) AND (STR_TO_DATE(NEW.contract_start, '%d.%m.%Y') < STR_TO_DATE(T.contract_finish, '%d.%m.%Y')))
    OR ((STR_TO_DATE(T.contract_start, '%d.%m.%Y') < STR_TO_DATE(NEW.contract_finish, '%d.%m.%Y')) AND (STR_TO_DATE(NEW.contract_finish, '%d.%m.%Y') <=  STR_TO_DATE(T.contract_finish, '%d.%m.%Y'))));

    IF coach_overlap > 0 THEN
        SET @error_message = CONCAT('Coach ', NEW.coach_username, " directs another team in given dates.");
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = @error_message;
    END IF;
END;
//

DELIMITER ;