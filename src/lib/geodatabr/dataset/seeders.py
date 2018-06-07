#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
'''
Dataset seeders module

This module provides the seeders classes used to populate the dataset.
'''
# Imports

# Package dependencies

from geodatabr.core.types import AbstractClass
from geodatabr.dataset import Database
from geodatabr.dataset.schema import \
    State, Mesoregion, Microregion, Municipality, District, Subdistrict
from geodatabr.dataset.repositories import \
    StateRepository, MesoregionRepository, MicroregionRepository, \
    MunicipalityRepository, DistrictRepository, SubdistrictRepository
from geodatabr.dataset.services import \
    SidraDataset, SIDRA_STATE, SIDRA_MESOREGION, SIDRA_MICROREGION, \
    SIDRA_MUNICIPALITY, SIDRA_DISTRICT, SIDRA_SUBDISTRICT

# Classes


class Seeder(AbstractClass):
    '''
    Abstract implementation of seeders.
    '''

    def __init__(self):
        '''
        Creates a new entity seeder instance.
        '''
        self._sidra = SidraDataset()

    def run(self, reset=False):
        '''
        Runs the database seeder.

        Args:
            reset (bool): Whether or not it should clear the existing table data
        '''
        raise NotImplementedError


class StateSeeder(Seeder):
    '''
    Database seeder for states.
    '''

    def run(self, reset=False):
        '''
        Runs the database seeder.

        Args:
            reset (bool): Whether or not it should clear the existing states
        '''
        if StateRepository.count() and not reset:
            return

        # Clear existing data
        StateRepository.clear()

        states = self._sidra.findAll(SIDRA_STATE)

        for state in states:
            StateRepository.add(
                State(id=state.id,
                      name=state.name))

        Database.commit()


class MesoregionSeeder(Seeder):
    '''
    Database seeder for mesoregions.
    '''

    def run(self, reset=False):
        '''
        Runs the database seeder.

        Args:
            reset (bool): Whether or not it should clear the existing mesoregions
        '''
        if MesoregionRepository.count() and not reset:
            return

        # Clear existing data
        MesoregionRepository.clear()

        states = StateRepository.findAll()

        for state in states:
            mesoregions = self._sidra \
                .findChildren(SIDRA_MESOREGION,
                              SIDRA_STATE,
                              state.id)

            for mesoregion in mesoregions:
                MesoregionRepository.add(
                    Mesoregion(id=mesoregion.id,
                               state_id=state.id,
                               name=mesoregion.name))

        Database.commit()


class MicroregionSeeder(Seeder):
    '''
    Database seeder for microregions.
    '''

    def run(self, reset=False):
        '''
        Runs the database seeder.

        Args:
            reset (bool): Whether or not it should clear the existing microregions
        '''
        if MicroregionRepository.count() and not reset:
            return

        # Clear existing data
        MicroregionRepository.clear()

        mesoregions = MesoregionRepository.findAll()

        for mesoregion in mesoregions:
            microregions = self._sidra \
                .findChildren(SIDRA_MICROREGION,
                              SIDRA_MESOREGION,
                              mesoregion.id)

            for microregion in microregions:
                MicroregionRepository.add(
                    Microregion(id=microregion.id,
                                state_id=mesoregion.state_id,
                                mesoregion_id=mesoregion.id,
                                name=microregion.name))

        Database.commit()


class MunicipalitySeeder(Seeder):
    '''
    Database seeder for microregions.
    '''

    def run(self, reset=False):
        '''
        Runs the database seeder.

        Args:
            reset (bool): Whether or not it should clear the existing municipalities
        '''
        if MunicipalityRepository.count() and not reset:
            return

        # Clear existing data
        MunicipalityRepository.clear()

        microregions = MicroregionRepository.findAll()

        for microregion in microregions:
            municipalities = self._sidra \
                .findChildren(SIDRA_MUNICIPALITY,
                              SIDRA_MICROREGION,
                              microregion.id)

            for municipality in municipalities:
                MunicipalityRepository.add(
                    Municipality(id=municipality.id,
                                 state_id=microregion.state_id,
                                 mesoregion_id=microregion.mesoregion_id,
                                 microregion_id=microregion.id,
                                 name=municipality.name))

        Database.commit()


class DistrictSeeder(Seeder):
    '''
    Database seeder for districts.
    '''

    def run(self, reset=False):
        '''
        Runs the database seeder.

        Args:
            reset (bool): Whether or not it should clear the existing districts
        '''
        if DistrictRepository.count() and not reset:
            return

        # Clear existing data
        DistrictRepository.clear()

        municipalities = MunicipalityRepository.findAll()

        for municipality in municipalities:
            districts = self._sidra \
                .findChildren(SIDRA_DISTRICT,
                              SIDRA_MUNICIPALITY,
                              municipality.id)

            for district in districts:
                DistrictRepository.add(
                    District(id=district.id,
                             state_id=municipality.state_id,
                             mesoregion_id=municipality.mesoregion_id,
                             microregion_id=municipality.microregion_id,
                             municipality_id=municipality.id,
                             name=district.name))

        Database.commit()


class SubdistrictSeeder(Seeder):
    '''
    Database seeder for subdistricts.
    '''

    def run(self, reset=False):
        '''
        Runs the database seeder.

        Args:
            reset (bool): Whether or not it should clear the existing subdistricts
        '''
        if SubdistrictRepository.count() and not reset:
            return

        # Clear existing data
        SubdistrictRepository.clear()

        districts = DistrictRepository.findAll()

        for district in districts:
            subdistricts = self._sidra \
                .findChildren(SIDRA_SUBDISTRICT,
                              SIDRA_DISTRICT,
                              district.id)

            for subdistrict in subdistricts:
                SubdistrictRepository.add(
                    Subdistrict(id=subdistrict.id,
                                state_id=district.state_id,
                                mesoregion_id=district.mesoregion_id,
                                microregion_id=district.microregion_id,
                                municipality_id=district.municipality_id,
                                district_id=district.id,
                                name=subdistrict.name))

        Database.commit()
