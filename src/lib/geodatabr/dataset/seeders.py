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

from geodatabr.core import decorators, types
from geodatabr.dataset import base, repositories, schema, services as sidra

# Classes


class Seeder(types.AbstractClass):
    """
    Abstract implementation of database seeders.

    Attributes:
        db (geodatabr.dataset.base.Database)
        session (sqlalchemy.orm.session.Session):
            The database session instance
        sidra_db (geodatabr.dataset.services.SidraDataset):
            The SIDRA dataset service instance
        entity (geodatabr.dataset.schema.Entity):
            The seeder entity class
        repository (geodatabr.dataset.repositories.Repository):
            The seeder repository class
    """

    db = base.Database
    session = db.session()
    sidra_db = sidra.SidraDataset()
    entity = None
    repository = None

    @classmethod
    @decorators.abstractmethod
    def run(cls):
        """Runs the database seeder."""
        raise NotImplementedError


class StateSeeder(Seeder):
    """
    Database seeder for states.

    Attributes:
        entity (geodatabr.dataset.schema.State):
            The states entity class
        repository (geodatabr.dataset.repositories.StateRepository):
            The states repository class
    """

    entity = schema.State
    repository = repositories.StateRepository

    @classmethod
    def run(cls):
        """
        Runs the database seeder.

        Raises:
            geodatabr.dataset.seeders.NothingToSeedError:
                If the states table is not empty
        """
        if cls.repository.count():
            raise NothingToSeedError

        states = cls.sidra_db.findAll(sidra.SIDRA_STATE)

        with cls.db.transaction(cls.session):
            for state in states:
                cls.repository.add(cls.entity(id=state.id,
                                              name=state.name))


class MesoregionSeeder(Seeder):
    """
    Database seeder for mesoregions.

    Attributes:
        entity (geodatabr.dataset.schema.Mesoregion):
            The mesoregions entity class
        repository (geodatabr.dataset.repositories.MesoregionRepository):
            The mesoregions repository class
        parent_repository (geodatabr.dataset.repositories.StateRepository):
            The states repository class
    """

    entity = schema.Mesoregion
    repository = repositories.MesoregionRepository
    parent_repository = repositories.StateRepository

    @classmethod
    def run(cls):
        """
        Runs the database seeder.

        Raises:
            geodatabr.dataset.seeders.NothingToSeedError:
                If the mesoregions table is not empty
        """
        if cls.repository.count():
            raise NothingToSeedError

        states = cls.parent_repository.findAll()

        with cls.db.transaction(cls.session):
            for state in states:
                mesoregions = cls.sidra_db \
                    .findChildren(sidra.SIDRA_MESOREGION,
                                  sidra.SIDRA_STATE,
                                  state.id)

                for mesoregion in mesoregions:
                    cls.repository.add(cls.entity(id=mesoregion.id,
                                                  state_id=state.id,
                                                  name=mesoregion.name))


class MicroregionSeeder(Seeder):
    """
    Database seeder for microregions.

    Attributes:
        entity (geodatabr.dataset.schema.Microregion):
            The microregions entity class
        repository (geodatabr.dataset.repositories.MicroregionReposiory):
            The microregions repository class
        parent_repository (geodatabr.dataset.repositories.MesoregionRepository):
            The mesoregions repository class
    """

    entity = schema.Microregion
    repository = repositories.MicroregionRepository
    parent_repository = repositories.MesoregionRepository

    @classmethod
    def run(cls):
        """
        Runs the database seeder.

        Raises:
            geodatabr.dataset.seeders.NothingToSeedError:
                If the microregions table is not empty
        """
        if cls.repository.count():
            raise NothingToSeedError

        mesoregions = cls.parent_repository.findAll()

        with cls.db.transaction(cls.session):
            for mesoregion in mesoregions:
                microregions = cls.sidra_db \
                    .findChildren(sidra.SIDRA_MICROREGION,
                                  sidra.SIDRA_MESOREGION,
                                  mesoregion.id)

                for microregion in microregions:
                    cls.repository.add(
                        cls.entity(id=microregion.id,
                                   state_id=mesoregion.state_id,
                                   mesoregion_id=mesoregion.id,
                                   name=microregion.name))


class MunicipalitySeeder(Seeder):
    """
    Database seeder for municipalities.

    Attributes:
        entity (geodatabr.dataset.schema.Municipality):
            The municipalities entity class
        repository (geodatabr.dataset.repositories.MunicipalityRepository):
            The municipalities repository class
        parent_repository (geodatabr.dataset.repositories.MicroregionRepository):
            The microregions repository class
    """

    entity = schema.Municipality
    repository = repositories.MunicipalityRepository
    parent_repository = repositories.MicroregionRepository

    @classmethod
    def run(cls):
        """
        Runs the database seeder.

        Raises:
            geodatabr.dataset.seeders.NothingToSeedError:
                If the municipalities table is not empty
        """
        if cls.repository.count():
            raise NothingToSeedError

        microregions = cls.parent_repository.findAll()

        with cls.db.transaction(cls.session):
            for microregion in microregions:
                municipalities = cls.sidra_db \
                    .findChildren(sidra.SIDRA_MUNICIPALITY,
                                  sidra.SIDRA_MICROREGION,
                                  microregion.id)

                for municipality in municipalities:
                    cls.repository.add(
                        cls.entity(id=municipality.id,
                                   state_id=microregion.state_id,
                                   mesoregion_id=microregion.mesoregion_id,
                                   microregion_id=microregion.id,
                                   name=municipality.name))


class DistrictSeeder(Seeder):
    """
    Database seeder for districts.

    Attributes:
        entity (geodatabr.dataset.schema.District):
            The districts entity class
        repository (geodatabr.dataset.repositories.DistrictRepository):
            The districts repository class
        parent_repository (geodatabr.dataset.repositories.MunicipalityRepository):
            The municipalities repository class
    """

    entity = schema.District
    repository = repositories.DistrictRepository
    parent_repository = repositories.MunicipalityRepository

    @classmethod
    def run(cls):
        """
        Runs the database seeder.

        Raises:
            geodatabr.dataset.seeders.NothingToSeedError:
                If the districts table is not empty
        """
        if cls.repository.count():
            raise NothingToSeedError

        municipalities = cls.parent_repository.findAll()

        with cls.db.transaction(cls.session):
            for municipality in municipalities:
                districts = cls.sidra_db \
                    .findChildren(sidra.SIDRA_DISTRICT,
                                  sidra.SIDRA_MUNICIPALITY,
                                  municipality.id)

                for district in districts:
                    cls.repository.add(
                        cls.entity(id=district.id,
                                   state_id=municipality.state_id,
                                   mesoregion_id=municipality.mesoregion_id,
                                   microregion_id=municipality.microregion_id,
                                   municipality_id=municipality.id,
                                   name=district.name))


class SubdistrictSeeder(Seeder):
    """
    Database seeder for subdistricts.

    Attributes:
        entity (geodatabr.dataset.schema.Subdistrict):
            The subdistricts entity class
        repository (geodatabr.dataset.repositories.SubdistrictRepository):
            The subdistricts repository class
        parent_repository (geodatabr.dataset.repositories.DistrictRepository):
            The districts repository class
    """

    entity = schema.Subdistrict
    repository = repositories.SubdistrictRepository
    parent_repository = repositories.DistrictRepository

    @classmethod
    def run(cls):
        """
        Runs the database seeder.

        Raises:
            geodatabr.dataset.seeders.NothingToSeedError:
                If the subdistricts table is not empty
        """
        if cls.repository.count():
            raise NothingToSeedError

        districts = cls.parent_repository.findAll()

        with cls.db.transaction(cls.session):
            for district in districts:
                subdistricts = cls.sidra_db \
                    .findChildren(sidra.SIDRA_SUBDISTRICT,
                                  sidra.SIDRA_DISTRICT,
                                  district.id)

                for subdistrict in subdistricts:
                    cls.repository.add(
                        cls.entity(id=subdistrict.id,
                                   state_id=district.state_id,
                                   mesoregion_id=district.mesoregion_id,
                                   microregion_id=district.microregion_id,
                                   municipality_id=district.municipality_id,
                                   district_id=district.id,
                                   name=subdistrict.name))


class SeederFactory(object):
    """Factory class for instantiation of concrete seeder classes."""

    @staticmethod
    def fromEntity(entity: schema.Entity) -> Seeder:
        """
        Factories a seeder class for a given entity class.

        Args:
            entity: The entity class to retrieve a seeder

        Returns:
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


class NothingToSeedError(Exception):
    """Exception class raised when a given entity table is not empty."""
