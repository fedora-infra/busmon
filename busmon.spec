%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get _python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

%define modname busmon

Name:           busmon
Version:        0.2.2
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
%if %{?rhel}%{!?rhel:0} >= 6
BuildRequires:  python-sqlalchemy0.7
%else
BuildRequires:  python-sqlalchemy
%endif
BuildRequires:  python-repoze-what
BuildRequires:  python-repoze-who-friendlyform
BuildRequires:  python-repoze-what-pylons
BuildRequires:  python-repoze-who
BuildRequires:  python-repoze-what-plugins-sql
BuildRequires:  python-kitchen
BuildRequires:  pycurl
BuildRequires:  python-tw2-core
BuildRequires:  python-tw2-forms
BuildRequires:  python-tw2-jqplugins-ui
BuildRequires:  python-tw2-jqplugins-gritter
BuildRequires:  python-docutils
BuildRequires:  python-bunch
BuildRequires:  python-fedora
BuildRequires:  python-fedora-turbogears2
BuildRequires:  fedmsg >= 0.1.5

Requires:       TurboGears2
Requires:       python-mako
Requires:       python-zope-sqlalchemy
%if %{?rhel}%{!?rhel:0} >= 6
Requires:  python-sqlalchemy0.7
%else
Requires:  python-sqlalchemy
%endif
Requires:       python-repoze-what
Requires:       python-repoze-who-friendlyform
Requires:       python-repoze-what-pylons
Requires:       python-repoze-who
#Requires:       python-repoze-what-quickstart
Requires:       python-repoze-what-plugins-sql
Requires:       python-kitchen
Requires:       pycurl
Requires:       python-tw2-d3
Requires:       fedmsg >= 0.1.5
Requires:       moksha-server >= 0.8.0

%description
A webapp for visualizing the Fedora Message Bus

%prep
%setup -q

%if %{?rhel}%{!?rhel:0} >= 6

# Make sure that epel/rhel picks up the correct version of webob
awk 'NR==1{print "import __main__; __main__.__requires__ = __requires__ = [\"WebOb>=1.0\", \"sqlalchemy>=0.7\"]; import pkg_resources"}1' setup.py > setup.py.tmp
mv setup.py.tmp setup.py

%endif


%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}
%{__python} setup.py archive_tw2_resources -f -o %%{buildroot}%{_datadir}/%{name}/public/toscawidgets -d busmon

rm -fr %{buildroot}%{python_sitelib}/migration

%{__mkdir_p} %{buildroot}%{_datadir}/%{name}/apache
%{__install} apache/%{modname}.wsgi %{buildroot}%{_datadir}/%{name}/apache/%{modname}.wsgi


%files
%doc README.rst
%{_datadir}/%{name}/
%{python_sitelib}/%{modname}/
%{python_sitelib}/%{modname}-%{version}-py%{pyver}.egg-info/

%changelog
* Mon Jun 04 2012 Ralph Bean <rbean@redhat.com> - 0.2.2-1
- Fork the spec from fedora-tagger.spec
