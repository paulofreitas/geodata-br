#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""
Dataset seeders module.

This module provides the seeders classes used to populate the dataset.
"""
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
    """
    Abstract implementation of database seeders.

    Attributes:
        db (sqlalchemy.orm.session.Session): The database session instance
        sidra (geodatabr.dataset.services.SidraDataset):
            The SIDRA dataset service instance
        entity (geodatabr.dataset.schema.Entity): The seeder entity class
    """

    db = Database.session()
    sidra = SidraDataset()
    entity = None

    @classmethod
    def run(cls):
        """Runs the database seeder."""
        raise NotImplementedError


class StateSeeder(Seeder):
    """Database seeder for states."""

    entity = State

    @classmethod
    def run(cls):
        """
        Runs the database seeder.

        Raises:
            geodatabr.dataset.seeders.NothingToSeedError:
                If the states table is not empty
        """
        if StateRepository.count():
            raise NothingToSeedError

        states = cls.sidra.findAll(SIDRA_STATE)

        with Database.transaction(cls.db):
            for state in states:
                StateRepository.add(State(id=state.id,
                                          name=state.name))


class MesoregionSeeder(Seeder):
    """Database seeder for mesoregions."""

    entity = Mesoregion

    @classmethod
    def run(cls):
        """
        Runs the database seeder.

        Raises:
            geodatabr.dataset.seeders.NothingToSeedError:
                If the mesoregions table is not empty
        """
        if MesoregionRepository.count():
            raise NothingToSeedError

        states = StateRepository.findAll()

        with Database.transaction(cls.db):
            for state in states:
                mesoregions = cls.sidra.findChildren(SIDRA_MESOREGION,
                                                     SIDRA_STATE,
                                                     state.id)

                for mesoregion in mesoregions:
                    MesoregionRepository.add(Mesoregion(id=mesoregion.id,
                                                        state_id=state.id,
                                                        name=mesoregion.name))


class MicroregionSeeder(Seeder):
    """Database seeder for microregions."""

    entity = Microregion

    @classmethod
    def run(cls):
        """
        Runs the database seeder.

        Raises:
            geodatabr.dataset.seeders.NothingToSeedError:
                If the microregions table is not empty
        """
        if MicroregionRepository.count():
            raise NothingToSeedError

        mesoregions = MesoregionRepository.findAll()

        with Database.transaction(cls.db):
            for mesoregion in mesoregions:
                microregions = cls.sidra.findChildren(SIDRA_MICROREGION,
                                                      SIDRA_MESOREGION,
                                                      mesoregion.id)

                for microregion in microregions:
                    MicroregionRepository.add(
                        Microregion(id=microregion.id,
                                    state_id=mesoregion.state_id,
                                    mesoregion_id=mesoregion.id,
                                    name=microregion.name))


class MunicipalitySeeder(Seeder):
    """Database seeder for municipalities."""

    entity = Municipality

    @classmethod
    def run(cls):
        """
        Runs the database seeder.

        Raises:
            geodatabr.dataset.seeders.NothingToSeedError:
                If the municipalities table is not empty
        """
        if MunicipalityRepository.count():
            raise NothingToSeedError

        microregions = MicroregionRepository.findAll()

        with Database.transaction(cls.db):
            for microregion in microregions:
                municipalities = cls.sidra.findChildren(SIDRA_MUNICIPALITY,
                                                        SIDRA_MICROREGION,
                                                        microregion.id)

                for municipality in municipalities:
                    MunicipalityRepository.add(
                        Municipality(id=municipality.id,
                                     state_id=microregion.state_id,
                                     mesoregion_id=microregion.mesoregion_id,
                                     microregion_id=microregion.id,
                                     name=municipality.name))


class DistrictSeeder(Seeder):
    """Database seeder for districts."""

    entity = District

    @classmethod
    def run(cls):
        """
        Runs the database seeder.

        Raises:
            geodatabr.dataset.seeders.NothingToSeedError:
                If the districts table is not empty
        """
        if DistrictRepository.count():
            raise NothingToSeedError

        municipalities = MunicipalityRepository.findAll()

        with Database.transaction(cls.db):
            for municipality in municipalities:
                districts = cls.sidra.findChildren(SIDRA_DISTRICT,
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


class SubdistrictSeeder(Seeder):
    """Database seeder for subdistricts."""

    entity = Subdistrict

    @classmethod
    def run(cls):
        """
        Runs the database seeder.

        Raises:
            geodatabr.dataset.seeders.NothingToSeedError:
                If the subdistricts table is not empty
        """
        if SubdistrictRepository.count():
            raise NothingToSeedError

        districts = DistrictRepository.findAll()

        with Database.transaction(cls.db):
            for district in districts:
                subdistricts = cls.sidra.findChildren(SIDRA_SUBDISTRICT,
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


class SeederFactory(object):
    """Factory class for instantiation of concrete seeder classes."""

    def __new__(cls, entity):
        """
        Factories a seeder class for a given entity class.

        Args:
            entity (geodatabr.dataset.schema.Entity):
                The entity class to retrieve a seeder

        Returns:
            geodatabr.dataset.seeders.Seeder:
                The seeder class instance

        Raises:
            geodatabr.dataset.seeders.UnknownEntityError:
                If a given entity is not supported
        """
        for seeder in Seeder.childs():
            if seeder.entity is entity:
                return seeder()

        raise UnknownEntityError(
            'No seeder for entity "{}"'.format(entity.__name__))


class UnknownEntityError(Exception):
    """
    Exception class raised when a given entity does not belong to any seeder.
    """
    pass


class NothingToSeedError(Exception):
    """Exception class raised when a given entity table is not empty."""
