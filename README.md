# Nursing-Home-Personalized-Matching-System-dsy

This project aims to design a website to help users with nursing needs match to Nursing homes that better meet their own
needs. Nursing home data is obtained from China Nursing Home Network by a crawler and stored in a sqlite database.
Front-end and back-end data interaction is realized through the flask framework, and echart Chart visualization

SELECT

    allergy_description,
    ROUND((male_count / total_count) * 100, 2) AS male_percentage,
    ROUND((female_count / total_count) * 100, 2) AS female_percentage

FROM (
SELECT
pa.allergy_description,
SUM(CASE WHEN p.gender = 'M' THEN 1 ELSE 0 END) AS male_count,
SUM(CASE WHEN p.gender = 'F' THEN 1 ELSE 0 END) AS female_count,
COUNT(*) AS total_count
FROM
hc848.MITRE_PATIENT_ALLERGY pa
JOIN
hc848.MITRE_PATIENT p ON pa.patient_id = p.patient_id
WHERE
pa.allergy_description IN ('Fish', 'Soya', 'Wheat')
GROUP BY
pa.allergy_description
) AS allergy_stats;