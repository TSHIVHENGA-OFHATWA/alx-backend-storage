-- Script to list all bands with Glam rock as their main style ranked by their longevity
SELECT band_name, 
       (IFNULL(split, '2020' - formed) AS lifespan
FROM metal_bands
WHERE main_style = 'Glam rock', IFNULL(style, "")) > 0
ORDER BY lifespan DESC;
