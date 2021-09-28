-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description FROM crime_scene_reports WHERE year = 2020 AND month = 7 AND day = 28 AND  street = "Chamberlin Street"; 
-- Get an understanding of the crime, ocurred at 10:15 am at the Court House, 3 witnesses all have interviews and mention "courthouse"

SELECT transcript FROM interviews WHERE year = 2020 AND month = 7 AND day = 28 AND transcript LIKE "%Courthouse%"; 
-- Get witness interviews to gain general understanding of the crime

SELECT DISTINCT name FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number WHERE day = "28" AND month = "7" AND year = "2020" AND transaction_type = "withdraw" AND atm_location = "Fifer Street";
-- Get names of people that withdrew money from the ATM at the witness metnioned time. The thief is among: Danielle, Bobby, Madison, Ernest, Roy, Elizabeth, Victoria, Russell

SELECT DISTINCT name FROM people JOIN courthouse_security_logs ON people.license_plate = courthouse_security_logs.license_plate WHERE year = 2020 AND month = 7 AND day = 28 AND minute < "25" AND minute >= "15" AND activity = "exit";
-- Get names of people that left the courthouse within ten minutes of the theft, names that align with the atm withdrawl are Ernest, Danielle, Russell, and Elizabeth

SELECT DISTINCT name FROM people JOIN phone_calls ON people.phone_number = phone_calls.caller WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60;
-- Get names of people that had a call for less than a minute on the day of theft. Out of the four current suspects only Ernest and Russell are left.

SELECT name FROM people JOIN passengers ON people.passport_number = passengers.passport_number WHERE flight_id = (SELECT id FROM flights WHERE year = 2020 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);
-- Get names of the people on the first flight out of fiftyville the next day of the theft which the thief is supposed be on. Ernest is on the flight but Russell isn't so Ernest is the thief.

SELECT name FROM people JOIN phone_calls ON people.phone_number = phone_calls.receiver WHERE caller = (SELECT phone_number FROM people WHERE name = "Ernest") AND year = 2020 AND month = 7 AND day = 28 AND duration < 60;
--Get the name of the person Ernest called for a minute on the day of the crime. This person, Berthold is the accomplice

SELECT city FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE year = 2020 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);
-- Get destination airport: London, England
