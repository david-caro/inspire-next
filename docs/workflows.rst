..
    This file is part of INSPIRE.
    Copyright (C) 2017 CERN.

    INSPIRE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    INSPIRE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.

    In applying this licence, CERN does not waive the privileges and immunities
    granted to it by virtue of its status as an Intergovernmental Organization
    or submit itself to any jurisdiction.



Ingestion of records (Workflows)
********************************


Inspire-next retrieves new records every day from several sources, such as:
    * External sites (arXiv, Proceedings of Science, ...).
    * Users, through submission forms.

The records harvested from external sites are all pulled in by `hepcrawl`_,
that is periodically executed by a `celery beat`_ task.

The Users also suggest new records, both literature records and author records
by using the submission forms.

One of the main goals of Inspire is the high quality of the information it
provides, so in order to achieve that, every record is carefully and rigorously
revised by our team of curators befor finally getting accepted inside the
Inspire database.

Below there's a small diagram summarizing the process.

.. image:: images/workflows_overview.png
    :height: 660
    :width: 660


.. _hepcrawl: https://github.com/inspirehep/hepcrawl
.. _celery beat: http://docs.celeryproject.org/en/latest/reference/celery.beat.html
