#!/usr/bin/env python3

__author__ = "Maria K Zurek <zurek@anl.gov>"


from dataclasses import dataclass, field
import logging
import math
import os
from pprint import pprint
import sys
from typing import List, Iterable, Dict, Callable, Tuple

from geometry import VARIATION_MAP
from materials import define_materials


_logger = logging.getLogger("compare_targets")


@dataclass
class VolumeParams:
    "Parses and stores G4 volume parameters from gemc2 and gemc3"
    original: str = field(repr=False)
    gemc_version: str
    tokens: List[str] = field(default_factory=list)
    name: str = None
    mother: str = None
    solid: str = None
    solid_parameters: str = None
    solid_parameters_numbers: List[str] = field(default_factory=list)
    solid_parameters_units: List[str] = field(default_factory=list)
    material: str = None
    position: str = None
    position_numbers: List[str] = field(default_factory=list)
    position_units: List[str] = field(default_factory=list)
    rotation: str = None
    rotation_numbers: List[str] = field(default_factory=list)
    rotation_units: List[str] = field(default_factory=list)
    mfield: str = None
    visibility: float = -1
    style: float = -1
    color: str = None
    digitization: str = None
    identifier: str = None
    copy_of: str = None
    replica_of: str = None
    solids_opr: str = None
    mirror: str = None
    exist: str = None
    description: str = None

    def __post_init__(self):
        s = self.original
        self.tokens = [
            tok.strip()
            for tok in s.split("|")
        ]
        map_reader = {
            "gemc2": self.read_gemc2,
            "gemc3": self.read_gemc3,
        }
        map_reader[self.gemc_version](self.tokens)

    def read_gemc3(self, tokens: List[str]):
        self.name = tokens[0]
        self.mother = tokens[1]
        self.solid = tokens[2]
        self.solid_parameters = tokens[3]
        sp = SolidParams(self.solid_parameters) 
        self.solid_parameters_numbers = sp.numbers
        self.solid_parameters_units = sp.units
        self.material = tokens[4]
        self.position = tokens[5]
        pp = SolidParams(self.position)
        self.position_numbers = pp.numbers
        self.position_units = pp.units
        self.rotation = tokens[6]
        rp = SolidParams(self.rotation)
        self.rotation_numbers = rp.numbers
        self.rotation_units = rp.units
        self.mfield = tokens[7]
        self.visibility = tokens[8]
        self.style = tokens[9]
        self.color = tokens[10]
        self.digitization = tokens[11]
        self.identifier = tokens[12]
        self.copy_of = tokens[13]
        self.replica_of = tokens[14]
        self.solids_opr = tokens[15]
        self.mirror = tokens[16]
        self.exist = tokens[17]
        self.description = tokens[18]

    def read_gemc2(self, tokens: List[str]):
        self.name = tokens[0]
        self.mother = tokens[1]
        self.solid = tokens[6]
        self.solid_parameters = tokens[7]
        sp = SolidParams(self.solid_parameters) 
        self.solid_parameters_numbers = sp.numbers
        self.solid_parameters_units = sp.units
        self.material = tokens[8]
        self.position = tokens[3]
        pp = SolidParams(self.position)
        self.position_numbers = pp.numbers
        self.position_units = pp.units
        self.rotation = tokens[4]
        rp = SolidParams(self.rotation)
        self.rotation_numbers = rp.numbers
        self.rotation_units = rp.units
        self.mfield = tokens[9]
        self.visibility = tokens[13]
        self.style = tokens[14]
        self.color = tokens[5]
        self.digitization = tokens[16]
        self.identifier = tokens[17]
        # self.copy_of = tokens[]  
        # self.replica_of = tokens[]
        # self.solids_opr = tokens[]
        # self.mirror = tokens[]
        self.exist = tokens[12]
        self.description = tokens[2]


@dataclass
class SolidParams:
    "Parses and stores solid parameters"
    original: str
    tokens: List[str] = field(default_factory=list)
    without_units: str = None
    numbers: List[float] = field(default_factory=list)
    units: List[str] = field(default_factory=list)

    def __post_init__(self):
        s = self.original
        self.tokens = s.replace(",", "").split()

        for tok in self.tokens:
            number_and_units = tok.split("*")
            if len(number_and_units) == 2:
                num, units = number_and_units
            else:
                num, units = tok, None
            self.numbers.append(float(num))
            self.units.append(units)


@dataclass
class MatcherResult:
    "Class for results of the matchers"
    is_equal: bool = None
    name: str = None
    a_attribute: str = None
    b_attribute: str = None


class SimpleAttributeMatchers:
    "Creates simple matchers between attributes of VolumeParam instances"
    def __init__(self, attribute_names):
        self.names = list(attribute_names)
        self.equal_matchers = [
            self.get_equal_matcher(name)
            for name in self.names
        ]
        self.is_close_matchers = [
            self.get_is_close_matcher(name)
            for name in self.names
        ]
        self.no_na_matchers = [
            self.get_no_na_matcher(name)
            for name in self.names
        ]


    def get_equal_matcher(self, name):
        "Create matcher function based on == comparison"
        def matches_attribute(a: VolumeParams, b: VolumeParams) -> MatcherResult:
            a_attribute = getattr(a, name)
            b_attribute = getattr(b, name)
            is_equal = a_attribute == b_attribute
            return MatcherResult(is_equal, name, a_attribute, b_attribute)
        matches_attribute.__name__ = f"matches_{name}"
        return matches_attribute


    def get_is_close_matcher(self, name):
        "Create matcher function based on float comparison with finite tolerance"
        def matches_attribute(a: VolumeParams, b: VolumeParams) -> MatcherResult:
            a_attribute = getattr(a, name)
            b_attribute = getattr(b, name)
            is_equal = all([
                math.isclose(a_nb, b_nb, rel_tol=1e-6)
                for (a_nb, b_nb) in zip(a_attribute, b_attribute)
            ])
            return MatcherResult(is_equal, name, a_attribute, b_attribute)
        matches_attribute.__name__ = f"matches_{name}"
        return matches_attribute


    def get_no_na_matcher(self, name):
        'Create matcher function for default values "na" and "no" for gemc2 and gemc3'
        def matches_attribute(gemc2: VolumeParams, gemc3: VolumeParams) -> MatcherResult:
            gemc2_attribute = getattr(gemc2, name)
            gemc3_attribute = getattr(gemc3, name)
            is_equal = (gemc2_attribute == "no" and gemc3_attribute == "na") or gemc2_attribute == gemc3_attribute
            return MatcherResult(is_equal, name, gemc2_attribute, gemc3_attribute)
        matches_attribute.__name__ = f"matches_{name}"
        return matches_attribute    


def matches_solid(gemc2: VolumeParams, gemc3: VolumeParams) -> MatcherResult:
    "Advanced matcher for solid types for gemc2 and gemc3"

    map_gemc3_solid_to_gemc2_solid = {
        "G4Box": "Box",
        "G4Tubs": "Tube",
        "G4Polycone": "Polycone",
        "G4Sphere": "Sphere"
    }
    gemc2_solid = gemc2.solid
    gemc3_solid = gemc3.solid
    is_equal = map_gemc3_solid_to_gemc2_solid[gemc3_solid] == gemc2_solid
    return MatcherResult(is_equal, "solid", gemc2_solid, gemc3_solid)


def matches_solid_numbers(gemc2: VolumeParams, gemc3: VolumeParams) -> MatcherResult:
    "Advanced matcher for solid parameter values for gemc2 and gemc3"
    g2_numbers = gemc2.solid_parameters_numbers
    g3_numbers = gemc3.solid_parameters_numbers

    # account for different order of polycone parameters in gemc2 and gemc3
    if gemc2.solid in {"Polycone"}:
        def get_chunk(lst, idx, size):
            return lst[size * idx:size * (idx + 1)]
        
        def get_chunks(numbers, size):
            return {
                idx: get_chunk(numbers[3:], idx, size)
                for idx in [0, 1, 2]
            }

        def compare_chunks(g2_chunk, g3_chunk):
            return all([
                math.isclose(g2_nb, g3_nb, rel_tol=1e-6)
                for (g3_nb, g2_nb) in zip(g3_chunk, g2_chunk)
            ])

        n_planes = int(g2_numbers[2])

        g2_chunks = get_chunks(g2_numbers, n_planes)
        g3_chunks = get_chunks(g3_numbers, n_planes)

        is_equal = all([
            math.isclose(g2_numbers[0], g3_numbers[0], rel_tol=1e-6),
            math.isclose(g2_numbers[1], g3_numbers[1], rel_tol=1e-6),
            g2_numbers[2] == g3_numbers[2],
            compare_chunks(g2_chunks[0], g3_chunks[1]),
            compare_chunks(g2_chunks[1], g3_chunks[2]),
            compare_chunks(g2_chunks[2],g3_chunks[0]),
        ])

    else:
        is_equal = all([
            math.isclose(g2_nb, g3_nb, rel_tol=1e-6)
            for (g3_nb, g2_nb) in zip(g3_numbers, g2_numbers)
        ]) 
    return MatcherResult(is_equal, "solid_numbers", g2_numbers, g3_numbers)


def matches_solid_units(gemc2: VolumeParams, gemc3: VolumeParams) -> MatcherResult:
    "Advanced matcher for solid parameter units for gemc2 and gemc3"
    g2_units = gemc2.solid_parameters_units
    g2_numbers = gemc2.solid_parameters_numbers
    g3_units = gemc3.solid_parameters_units

    # account for different order of polycone parameters
    # and different units for nplanes in gemc2 and gemc3
    if gemc2.solid in {"Polycone"}:
        def get_chunk(lst, idx, size):
            return lst[size * idx:size * (idx + 1)]
        
        def get_chunks(units, size):
            return {
                idx: get_chunk(units[3:], idx, size)
                for idx in [0, 1, 2]
            }

        n_planes = int(g2_numbers[2])

        g2_chunks = get_chunks(g2_units, n_planes)
        g3_chunks = get_chunks(g3_units, n_planes)

        is_equal = all([
            g2_units[0] == g3_units[0],
            g2_units[1] == g3_units[1],
            g2_chunks[0] == g3_chunks[1],
            g2_chunks[1] == g3_chunks[2],
            g2_chunks[2] == g3_chunks[0],
        ])

    else:
        is_equal = g3_units == g2_units
    return MatcherResult(is_equal, "solid_units", g2_units, g3_units)


def matches_position_units(gemc2: VolumeParams, gemc3: VolumeParams) -> MatcherResult:
    "Advanced matcher for position units"
    g2_units = gemc2.position_units
    g2_numbers = gemc2.position_numbers
    g3_units = gemc3.position_units
    is_equal = all([
        (g2_unit == g3_unit) or ((g2_unit == None) and (g2_number == 0))
        for (g2_unit, g2_number, g3_unit) in zip(g2_units, g2_numbers, g3_units)
    ])
    return MatcherResult(is_equal, "position_units", g2_units, g3_units)


def matches_rotation_units(gemc2: VolumeParams, gemc3: VolumeParams) -> MatcherResult:
    "Advanced matcher for position units"
    g2_units = gemc2.rotation_units
    g2_numbers = gemc2.rotation_numbers
    g3_units = gemc3.rotation_units
    is_equal = all([
        (g2_unit == g3_unit) or ((g2_unit == None) and (g2_number == 0))
        for (g2_unit, g2_number, g3_unit) in zip(g2_units, g2_numbers, g3_units)
    ])
    return MatcherResult(is_equal, "rotation_units", g2_units, g3_units)


def read_file(
        input_file_name,
        file_type,
    ) -> Iterable[VolumeParams]:

    with open(input_file_name) as f:
        return [
           VolumeParams(line, file_type)
           for line in f.readlines()
        ]


def get_indexed_volumes(items: Iterable[VolumeParams]) -> Dict[str, VolumeParams]:
    return {
        vp.name: vp
        for vp in items
    }


def compare_indexed_volumes(
        gemc2_volumes: Iterable[VolumeParams],
        gemc3_volumes: Iterable[VolumeParams],
        matchers: Iterable[Callable]
    ) -> Dict[str, Dict[Callable, MatcherResult]]:

    all_results = {}
    for volume_id, gemc2_vol in gemc2_volumes.items():
        _logger.info(f"comparing volume: {volume_id}")
        gemc3_vol = gemc3_volumes.get(volume_id, None)
        if gemc3_vol is None:
            _logger.warn(f'\nVolume "{volume_id}" not found in gemc3\n')
            continue
        match_results = {}
        for func in matchers:
            match_results[func.__name__] = func(
                gemc2_vol,
                gemc3_vol,
            )
        all_results[volume_id] = match_results
        for matcher, match_res in match_results.items():
            if not match_res.is_equal:
                _logger.warn(f"For volume {volume_id}, matcher {matcher}: {match_res}")
    return all_results


def compare_files(gemc2: os.PathLike, gemc3: os.PathLike) -> Dict[str, Dict[Callable, MatcherResult]]:
    gemc2_vols = read_file(gemc2, "gemc2")
    gemc3_vols = read_file(gemc3, "gemc3")

    simple_equal_matchers = SimpleAttributeMatchers([
        "mother", 
        "material", 
        "visibility",
        "color",
        "exist"
    ]).equal_matchers

    simple_is_close_matchers = SimpleAttributeMatchers([
        "position_numbers", 
        "rotation_numbers", 
    ]).is_close_matchers

    simple_no_na_matchers = SimpleAttributeMatchers([
        "mfield",
        "digitization",
        "identifier"
    ]).no_na_matchers

    advanced_matchers = [
        matches_solid,
        matches_solid_numbers,
        matches_solid_units,
        matches_position_units,
        matches_rotation_units,
    ]
    results = compare_indexed_volumes(
        get_indexed_volumes(gemc2_vols),
        get_indexed_volumes(gemc3_vols),
        simple_equal_matchers + simple_is_close_matchers + simple_no_na_matchers + advanced_matchers
    )
    return results


def get_target_pairs_to_compare(
        gemc2_prefix: str ="",
        gemc3_prefix: str = "",
        suffix: str = ".txt") -> Iterable[Tuple[os.PathLike, os.PathLike]]:
    map_gemc2_to_gemc3 = {
        "lH2": "lh2",
        "lD2": "ld2",
        "ND3": "nd3",
        "PolTarg": "pol_targ",
        "APOLLOnh3": "apollo_nh3",
        "APOLLOnd3": "apollo_nd3",
        "12C": "c12",
        "63Cu": "cu63",
        "118Sn": "sn118",
        "208Pb": "pb208",
        "27Al": "al27",
        "lH2e": "lh2e",
        "bonus": "bonus",
        "pbTest": "pb_test",
        "bonusb": "bonus",
        "hdIce": "hdice",
        "longitudinal": "longitudinal",
        "transverse": "transverse",
    }

    return [
        (f"{gemc2_prefix}{gemc2}{suffix}", f"{gemc3_prefix}{gemc3}{suffix}")
        for (gemc2, gemc3) in map_gemc2_to_gemc3.items()
    ]


def main():
    logging.basicConfig(level=logging.DEBUG)

    file_pairs_to_compare = get_target_pairs_to_compare(
        "./comparison-data/gemc2/target__geometry_",
        "./clas12Target__geometry_",
    )
    for gemc2_file, gemc3_file in file_pairs_to_compare:
        print("\n\n")
        _logger.info(f"{gemc2_file} -> {gemc3_file}")
        single_file_pair_results = compare_files(
            gemc2_file,
            gemc3_file,
        )
        #pprint(single_file_pair_results)


if __name__ == "__main__":
    main()

