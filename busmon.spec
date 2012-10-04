%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get _python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

%define modname busmon

Name:           busmon
Version:        0.4.1
Release:        1%{?dist}
Summary:        A webapp for visualizing the Fedora Message Bus

License:        LGPLv2
URL:            https://github.com/ralphbean/busmon
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel
BuildRequires:  libcurl-devel
BuildRequires:  python-kitchen
BuildRequires:  python-nose
BuildRequires:  python-paste
BuildRequires:  python-paste-deploy
BuildRequires:  TurboGears2
BuildRequires:  python-pylons
BuildRequires:  python-mako
BuildRequires:  python-zope-sqlalchemy
BuildRequires:  python-migrate
%if %{?rhel}%{!?rhel:0} >= 6
BuildRequires:  python-sqlalchemy0.7
%else
BuildRequires:  python-sqlalchemy
%endif
BuildRequires:  python-repoze-what
BuildRequires:  python-repoze-who-friendlyform
BuildRequires:  python-repoze-what-pylons
BuildRequires:  python-repoze-who
BuildRequires:  python-kitchen
BuildRequires:  pycurl
BuildRequires:  python-tw2-d3
BuildRequires:  python-bunch
BuildRequires:  python-fedora
BuildRequires:  python-fedora-turbogears2
%if %{?rhel}%{!?rhel:0} <= 6
BuildRequires:  python-ordereddict
%endif
BuildRequires:  python-moksha-wsgi >= 1.0.5

Requires:       TurboGears2
Requires:       python-mako
Requires:       python-zope-sqlalchemy
Requires:       python-migrate
%if %{?rhel}%{!?rhel:0} >= 6
Requires:       python-sqlalchemy0.7
%else
Requires:       python-sqlalchemy
%endif
Requires:       python-repoze-what
Requires:       python-repoze-who-friendlyform
Requires:       python-repoze-what-pylons
Requires:       python-repoze-who
Requires:       python-repoze-what-plugins-sql
Requires:       python-kitchen
Requires:       pycurl
Requires:       python-tw2-d3
%if %{?rhel}%{!?rhel:0} <= 6
Requires:       python-ordereddict
%endif
Requires:       python-moksha-wsgi >= 1.0.5

%description
A webapp for visualizing the Fedora Message Bus

%prep
%setup -q

# The old switch-a-roo
sed -i "s/WebOb==1.0.8/WebOb<=1.1.1/g" setup.py
sed -i '/\"tg.devtools\"/d' setup.py
sed -i '/\"repoze.tm\"/d' setup.py

%if %{?rhel}%{!?rhel:0} >= 6
# Make sure that epel/rhel picks up the correct version of webob
awk 'NR==1{print "import __main__; __main__.__requires__ = __requires__ = [\"WebOb>=1.0\", \"sqlalchemy>=0.7\"]; import pkg_resources"}1' setup.py > setup.py.tmp
mv setup.py.tmp setup.py
%endif


%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root=%{buildroot}

rm -fr %{buildroot}%{python_sitelib}/migration

%{__mkdir_p} %{buildroot}%{_datadir}/%{name}/apache
%{__install} apache/%{modname}.wsgi %{buildroot}%{_datadir}/%{name}/apache/%{modname}.wsgi


%{__mkdir_p} %{buildroot}%{_datadir}/%{name}/public/toscawidgets
%{__python} setup.py archive_tw2_resources -f -o %{buildroot}%{_datadir}/%{name}/public/toscawidgets -d busmon

# These next three lines are a temporary hack.
# The above archive_tw2_resources line SHOULD copy over moksha.js, but for some
# reason, its not happening during the rpm build process (it does work when you
# run it by hand).  So, to workaround, we just copy the file we need directly
# from the python-moksha-wsgi install.
mkdir -p %{buildroot}%{_datadir}/%{name}/public/toscawidgets/resources/moksha.wsgi.widgets.moksha_js/static
cp %{python_sitelib}/moksha/wsgi/widgets/static/* %{buildroot}%{_datadir}/%{name}/public/toscawidgets/resources/moksha.wsgi.widgets.moksha_js/static/.


%files
%doc README.rst
%{python_sitelib}/%{modname}/
%{python_sitelib}/%{modname}-%{version}*

%{_datadir}/%{name}/
# Just for verification's sake.
%{_datadir}/%{name}/public/toscawidgets/resources/moksha.wsgi.widgets.moksha_js/static/moksha.js
%{_datadir}/%{name}/public/toscawidgets/resources/tw2.jqplugins.gritter/static/jquery/gritter/js/jquery.gritter.min.js

%changelog
* Thu Oct 04 2012 Ralph Bean <rbean@redhat.com> - 0.4.1-1
- Bump for bugfixes.

* Fri Sep 28 2012 Ralph Bean <rbean@redhat.com> - 0.4.0-1
- Forked consumer out to busmon-consumers package.

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
