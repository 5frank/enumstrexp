#ifndef TESTENUMS_INCLUDE_H_
#define TESTENUMS_INCLUDE_H_

enum testenum_simple_e
{
  testenum_simple_00,
  testenum_simple_01,
  testenum_simple_02,
  testenum_simple_LAST
};


/// negative valeus and jumps (i.e. not continous)
enum testenum_negjmp_e
{
  testenum_negjmp_An33 = -33,
  testenum_negjmp_Bn3 = -3,
  testenum_negjmp_C00 = 0,
  testenum_negjmp_D01 = 1,
  testenum_negjmp_E04 = 4,
  testenum_negjmp_F1337 = 1337,
  testenum_negjmp_LAST
};
typedef enum testenum_negjmp_e testenum_negjmp_t;

enum
{
  anonEnum_A,
  anonEnum_B,
  anonEnum_C,
};

typedef enum
{
  noTagTypedef_A,
  noTagTypedef_B,
  noTagTypedef_C,
} noTagTypedef_e;

typedef enum tagAndTypedef_e
{
  tagAndTypedef_A,
  tagAndTypedef_B,
  tagAndTypedef_C,
} tagAndTypedef_e;


enum tagAndSepTypedef_e
{
  tagAndSepTypedef_A,
  tagAndSepTypedef_B,
  tagAndSepTypedef_C,
};

typedef enum tagAndSepTypedef_e tagAndSepTypedef_e;

// fits in 32-bit
enum testenum_flg32_e
{
  testenum_flg32_00 = (1u <<  0),
  testenum_flg32_01 = (1u <<  1),
  testenum_flg32_02 = (1u <<  2),
  testenum_flg32_03 = (1u <<  3),
  testenum_flg32_04 = (1u <<  4),
  testenum_flg32_05 = (1u <<  5),
  testenum_flg32_06 = (1u <<  6),
  testenum_flg32_07 = (1u <<  7),
  testenum_flg32_08 = (1u <<  8),
  testenum_flg32_09 = (1u <<  9),
  testenum_flg32_10 = (1u << 10),
  testenum_flg32_11 = (1u << 11),
  testenum_flg32_12 = (1u << 12),
  testenum_flg32_13 = (1u << 13),
  testenum_flg32_14 = (1u << 14),
  testenum_flg32_15 = (1u << 15),
  testenum_flg32_16 = (1u << 16),
  testenum_flg32_17 = (1u << 17),
  testenum_flg32_18 = (1u << 18),
  testenum_flg32_19 = (1u << 19),
  testenum_flg32_20 = (1u << 20),
  testenum_flg32_21 = (1u << 21),
  testenum_flg32_22 = (1u << 22),
  testenum_flg32_23 = (1u << 23),
  testenum_flg32_24 = (1u << 24),
  testenum_flg32_25 = (1u << 25),
  testenum_flg32_26 = (1u << 26),
  testenum_flg32_27 = (1u << 27),
  testenum_flg32_28 = (1u << 28),
  testenum_flg32_29 = (1u << 29),
  testenum_flg32_30 = (1u << 30),
  testenum_flg32_31 = (1u << 31)
};

#endif
