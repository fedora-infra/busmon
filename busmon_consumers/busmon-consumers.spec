%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get _python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

%define modname busmon_consumers

Name:           busmon-consumers
Version:        0.4.1
Release:        1%{?dist}
Summary:        fedmsg-hub consumers for the busmon webapp

License:        LGPLv2
URL:            https://github.com/ralphbean/busmon
Source0:        %{modname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel
BuildRequires:  python-pygments
BuildRequires:  fedmsg >= 0.5.0
BuildRequires:  python-paste-script

Requires:  python-pygments
Requires:  fedmsg >= 0.5.0
Requires:  python-paste-script

%description
fedmsg-hub consumers for the busmon webapp

%prep
%setup -q -n %{modname}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root=%{buildroot}

%files
%{python_sitelib}/%{modname}/
%{python_sitelib}/%{modname}-%{version}*

%changelog
* Thu Oct 04 2012 Ralph Bean <rbean@redhat.com> - 0.4.1-1
- Bump for bugfixes.

* Fri Sep 28 2012 Ralph Bean <rbean@redhat.com> - 0.4.0-1
- Fork from the busmon main package to separate dependencies.

* Fri Sep 28 2012 Ralph Bean <rbean@redhat.com> - 0.3.3-2
- Try to workaround broken archive_tw2_resources by copying moksha.js into the
  archive manually.

* Fri Sep 28 2012 Ralph Bean <rbean@redhat.com> - 0.3.3-1
- Include README.rst.

* Fri Sep 28 2012 Ralph Bean <rbean@redhat.com> - 0.3.2-5
- Rely on python-moksha-wsgi >= 1.0.5
- Removed BR on sql plugin and docutils.

* Fri Sep 28 2012 Ralph Bean <rbean@redhat.com> - 0.3.2-4
- Reenabled the file check for moksha.js.  Frustrating.

* Thu Sep 27 2012 Ralph Bean <rbean@redhat.com> - 0.3.2-3
- Commented out the extra file check for moksha.js.  Frustrating.

* Wed Sep 26 2012 Ralph Bean <rbean@redhat.com> - 0.3.2-2
- Depend on the latest fedmsg.

* Wed Sep 26 2012 Ralph Bean <rbean@redhat.com> - 0.3.2-1
- Depend on the latest moksha.
- Updated location of moksha.wsgi.widgets.moksha_js.

* Thu Aug 23 2012 Ralph Bean <rbean@redhat.com> - 0.3.1-1
- Modernize consumer setup.

* Wed Aug 22 2012 Ralph Bean <rbean@redhat.com> - 0.3.0-1
- Bugfix updates now that we can see it in stg.

* Wed Jul 18 2012 Ralph Bean <rbean@redhat.com> - 0.2.5-4
- Bugfix to archiving moksha resources.

* Wed Jul 18 2012 Ralph Bean <rbean@redhat.com> - 0.2.5-1
- Compat with older TurboGears for production
- Archiving moksha resources as well as busmon

* Wed Jul 18 2012 Ralph Bean <rbean@redhat.com> - 0.2.4-1
- Ripped out busmon.model and sqlalchemy deps.  Unnecessary.
- Removed dep on moksha-server.

* Tue Jul 17 2012 Ralph Bean <rbean@redhat.com> - 0.2.3-1
- Tweaks to the build process.
- Removed hard dep on pylons version.
- Removed hard dep on tg.devtools.
- Added dep on python-migrate
- BR on python-tw2-d3
- Loosened version constraint on repoze.tm

* Mon Jun 04 2012 Ralph Bean <rbean@redhat.com> - 0.2.2-1
- Fork the spec from fedora-tagger.spec
