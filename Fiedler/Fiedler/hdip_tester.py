
import pygraphblas as gb
import laplacian as lap
from hdip_fiedler import hdip_fiedler
from operator import itemgetter
matrixId=[
    2758, 2759, 904, 2760, 905,1438,1524, 13, 2761, 2203, 2399, 2204, 97, 14, 1177, 103, 133, 906, 1519, 1490, 1498, 129, 436, 872, 873, 874, 2396, 132, 1492, 1497, 2457, 106, 1484, 337, 23, 883, 2762,15,
    2400, 11, 136, 102, 220, 108, 907, 298, 2417, 2389, 2403, 2416, 323, 1630, 1631, 239, 113, 2397, 93, 94, 877, 878, 119, 1198, 95, 2763, 16, 17, 117, 2361, 2369, 2, 116, 202, 231, 96, 2748, 884, 875, 876,
    2205, 8, 251, 2421, 926, 27, 207, 122, 206, 3, 121, 100, 1634, 1635, 2749, 203, 929, 2206, 2362, 2370, 2207, 98, 124, 99, 908, 471, 472, 473, 4, 222, 2691, 114, 125, 2429, 26, 2431, 101, 204, 2750, 338, 1,
    2407, 278, 279, 281, 167, 1529, 406, 24, 325, 2751, 2754, 223, 1636, 2208, 300, 301, 302, 303, 304, 305, 2752, 2764, 2755, 2753, 130, 2436, 2420, 221, 205, 18, 2363, 2371, 2665, 2406, 333, 229, 19, 226, 134,    127, 20, 2465, 176, 21, 105, 41, 225, 177, 194, 2730, 2423, 104, 62, 135, 1628, 1629, 178, 1106, 1107, 138, 137, 182, 183, 159, 180, 28, 29, 299, 494, 495, 496, 2428, 2209, 2689, 111, 110, 195, 1188, 2195,
    2196, 1442, 181, 1239, 1790, 2690, 184, 475, 479, 477, 482, 476, 481, 474, 478, 179, 230, 107, 2364, 2372, 112, 1619, 196, 1430, 2408, 909, 515, 517, 516, 518, 511, 512, 514, 331, 1632, 1506, 91, 2419, 2466,    92, 2210, 1196, 2418, 197, 539, 1530, 2404, 2531, 227, 2765, 324, 2692, 1537, 198, 2666, 2422, 219, 139, 1360, 199, 31, 1633, 418, 830, 831, 540, 506, 507, 508, 509, 510, 521, 1539, 200, 828, 829, 339, 1538,    22, 241, 419, 498, 503, 497, 501, 500, 505, 499, 504, 2412, 201, 2731, 344, 422, 2467, 2411, 120, 358, 2706, 2410, 327, 416, 2409, 527, 2732, 332, 2522, 48, 1547, 1546, 1542, 871, 434, 530, 2667, 228, 1187,
    357, 1545, 1444, 1543, 531, 2668, 2670, 2669, 1206, 1448, 1449, 424, 2671, 2672, 469, 470, 480, 491, 502, 513, 524, 533, 534, 535, 363, 757, 2733, 483, 484, 485, 486, 487, 488, 489, 490, 492, 493, 532, 866,
    910, 2211, 420, 1548, 2766, 359, 45, 865, 1190, 421, 2405, 437, 2468, 1250, 1544, 1425, 2104, 427, 1551, 1552, 49, 77, 2663, 2425, 2424, 522, 523, 2415, 2414, 1245, 1554, 2850, 1191, 1553, 2523, 1549, 412,
    1555, 377, 1432, 1433, 417, 1234, 1217, 442, 2430, 2197, 2198, 758, 1214, 1242, 1556, 411, 1215, 425, 1557, 1550, 410, 443, 1216, 2707, 1559, 528, 529, 1192, 35, 2433, 444, 1563, 887, 888, 889, 1916, 1917,
    2520, 1249, 2413, 441, 2693, 2432, 1380, 1303, 2521, 2390, 1183, 2469, 2440, 2527, 440, 1437, 1441, 1262, 763, 881, 365, 760, 1193, 867, 2643, 1561, 2638, 2569, 1426, 2589, 1558, 868, 2636, 791, 792, 869,
    1194, 1565, 969, 870, 2767, 1443, 2437, 1247, 1248, 2537, 378, 2434, 2438, 2694, 1272, 1295, 911, 2533, 2695, 2627, 46, 2708, 1567, 1365, 364, 759, 1564, 1204, 1205, 1447, 832, 833, 2530, 2634, 2470, 2435,
    2709, 1366, 1312, 1854, 2632, 1611, 2710, 1907, 1255, 1566, 2711, 2712, 1608, 1610, 1609, 2269, 2270, 2271, 2272, 50, 2713, 2714, 2715, 2716, 2717, 1309, 2611, 970, 808, 2829, 2515, 1348, 2532, 1847, 886,
    1293, 1605, 1607, 1606, 2538, 1428, 1429, 2644, 1908, 814, 815, 2199, 2200, 1261, 1302, 379, 933, 1358, 1577, 350, 2332, 2261, 2262, 2602, 2588, 1330, 1292, 927, 1291, 343, 445, 541, 842, 2645, 2641, 2471,
    766, 767, 768, 769, 770, 771, 772, 773, 774, 1220, 1873, 2768, 775, 2622, 2614, 879, 1306, 2536, 2631, 1237, 1851, 1224, 1300, 2811, 1316, 776, 435, 885, 326, 1288, 777, 1222, 778, 1381, 1305, 1210, 1451,
    1311, 779, 1422, 1263, 1445, 2212, 2213, 1246, 912, 1289, 2625, 1307, 780, 55, 752, 753, 2635, 2609, 781, 2607, 1294, 1227, 2630, 1912, 1379, 891, 892, 782, 2601, 1587, 950, 2257, 2258, 1913, 1184, 765,
    1394, 1412, 2594, 2426, 1363, 1244, 1230, 1256, 924, 1347, 2600, 2472, 848, 783, 2525, 2612, 2613, 2606, 2646, 1359, 2621, 1914, 1915, 2584, 2528, 2610, 1415, 2628, 1259, 351, 366, 784, 2587, 847, 2618,
    2599, 1301, 2575, 2576, 813, 1202, 1435, 2593, 1848, 409, 2639, 2597, 342, 362, 341, 1892, 785, 2623, 2585, 2629, 1296, 2604, 2769, 361, 2583, 2617, 953, 1590, 2596, 817, 1368, 2526, 786, 890, 2626, 2608,
    2591, 1900, 340, 1452, 2518, 816, 1297, 788, 787, 789, 790, 1308, 2473, 2603, 855, 2461, 1231, 1383, 1919, 2605, 844, 845, 1251, 1434, 821, 822, 820, 1878, 352, 367, 1213, 2616, 804, 2778, 811, 2788, 1271,
    1417, 1284, 2462, 1643, 54, 913, 52, 2619, 846, 2779, 2427, 964, 965, 966, 967, 2517, 536, 2595, 851, 1357, 1235, 2460, 1287, 928, 853, 2642, 1286, 2570, 852, 356, 761, 368, 1431, 1236, 1382, 2260, 1274,
    973, 1282, 805, 2510, 849, 2474, 803, 854, 936, 2529, 1354, 1852, 2830, 1849, 1853, 1276, 2770, 1909, 1906, 1278, 1277, 2439, 850, 2283, 537, 856, 2373, 1208, 1209, 1450, 1275, 1283, 2624, 1898, 1910, 1423,
    2516, 1883, 1882, 1899, 1361, 1893, 1861, 1454, 1352, 2783, 1350, 2580, 2475, 2812, 859, 2519, 971, 937, 914, 858, 1421, 1349, 2813, 1355, 1356, 1290, 2265, 2266, 1351, 2571, 538, 1393, 1269, 2267, 2268,
    1385, 1257, 1254, 1364, 2771, 1367, 1219, 1260, 369, 1264, 1285, 2831, 1265, 2476, 1857, 2572, 2483, 2514, 1258, 938, 860, 1362, 2498, 2513, 2486, 1580, 1581, 1582, 1583, 1584, 1585, 940, 941, 942, 943,
    944, 945, 946, 947, 948, 1353, 2487, 1398, 2579, 2488, 2329, 2577, 2578, 2512, 2581, 2477, 2385, 2509, 2573, 1411, 915, 2495, 1901, 939, 1856, 2464, 2463, 2387, 2772, 2458, 2484, 1267, 1455, 2485, 2386,
    2478, 1586, 2480, 2459, 2854, 2481, 2482, 2781, 1252, 2496, 2388, 1902, 916, 2773, 2479, 2511, 2544, 1903, 2782, 2774, 1904, 1905, 2775, 2776, 2780, 2856]
#J=sorted(list(gb.Matrix.ssget(13)), key=itemgetter(0))[0]
#J[1].print(level=3)
#O=sorted(list(gb.Matrix.ssget(2024)), key=itemgetter(0))[0]
#O[1].print(level=3)
for mid in matrixId:
    J=sorted(list(gb.Matrix.ssget(mid)), key=itemgetter(0))[0]
    #J[1].print(level=3)
    pattern=J[1].pattern(gb.types.FP64)
    h=pattern+pattern.transpose()
    omega=lap.laplacian(pattern)
    #omega.print(level=3)
    hdip2=hdip_fiedler(omega)
    print(hdip2)
    print("The id of the matrix")
    print(mid)
    print("The first vector that is returned in the tuple")
    hdip2[0].print(level=3)
    print("The value that is returned for lambda")
    print(hdip2[1])
    print("The following are the values inside the iters tuple")
    print(hdip2[2][0])
    print("The second value inside the iters tuple")
    print(hdip2[2][1])
    wait = input("Press Enter to continue.")
print("check out 13 and 2204")
~                                  