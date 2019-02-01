/* Vectorization of the TURTLE/ECEF functions */

void turtle_ecef_from_geodetic_v(double * latitude, double * longitude,
    double * elevation, double * ecef, long n)
{
        for (; n > 0; n--, latitude++, longitude++, elevation++, ecef += 3) {
                turtle_ecef_from_geodetic(
                    *latitude, *longitude, *elevation, ecef);
        }
}
