#!/usr/bin/env python
# Author P G Jones - 12/05/2012 <p.g.jones@qmul.ac.uk> : First revision
# The CLHEP packages base class
import LocalPackage
import os
import PackageUtil

class Clhep( LocalPackage.LocalPackage ):
    """ Base clhep installer, different versions only have different names."""
    def __init__( self, name, tarName ):
        """ Initialise the clhep package."""
        super( Clhep, self ).__init__( name )
        self._TarName = tarName
        return
    def _IsDownloaded( self ):
        """ Check if downloaded."""
        return os.path.exists( os.path.join( PackageUtil.kCachePath, self._TarName ) )
    def _IsInstalled( self ):
        """ Check if installed."""
        return PackageUtil.LibraryExists( os.path.join( self.GetInstallPath(), "lib" ), "libCLHEP" )
    def _Download( self ):
        """ Derived classes should override this to download the package. Return True on success."""
        self._DownloadPipe += PackageUtil.DownloadFile( "http://proj-clhep.web.cern.ch/proj-clhep/DISTRIBUTION/tarFiles/" + self._TarName )
        return
#class ClhepPre??
    def GetDependencies( self ):
        """ Return the dependency names as a list of names."""
        return [ "make", "g++", "gcc" ]
    def _Install( self ):
        """ Install clhep."""
        self._InstallPipe += PackageUtil.UnTarFile( self._TarName, self.GetInstallPath(), 2 )
        self._InstallPipe += PackageUtil.ExecuteSimpleCommand( './configure', ['--prefix=%s' % self.GetInstallPath() ], 
                                                               None, self.GetInstallPath() )
        self._InstallPipe += PackageUtil.ExecuteSimpleCommand( 'make', [], None, self.GetInstallPath() )
        self._InstallPipe += PackageUtil.ExecuteSimpleCommand( 'make', ["install"], None, self.GetInstallPath() )
        return 

class ClhepPost2110( Clhep ):
    """ Base clhep installer for packages post 2.1.1.0."""
    def __init__( self, name, tarName ):
        """ Initialise clhep installer."""
        super( ClhepPost2110, self ).__init__( name, tarName )
        return
    def GetDependencies( self ):
        """ Return the dependency names as a list of names."""
        return [ "cmake", "make", "g++", "gcc" ]
    def _Install( self ):
        """ Install clhep, using cmake."""
        sourcePath = os.path.join( PackageUtil.kInstallPath, "%s-source" % self._Name )
        PackageUtil.UnTarFile( self._SourceTar, sourcePath, 2 )
        if not os.path.exists( self.GetInstallPath() ):
            os.makedirs( self.GetInstallPath() )
        cmakeOpts = [ "-DCMAKE_INSTALL_PREFIX=%s" % self.GetInstallPath() ]
        cmakeOpts.extend( [ sourcePath ] )
        cmakeCommand = "cmake"
        if self._DependencyPaths["cmake"] is not None: # Special cmake installed
            cmakeCommand = "%s/bin/cmake" % self._DependencyPaths["cmake"]
        self._InstallPipe += PackageUtil.ExecuteSimpleCommand( cmakeCommand, cmakeOpts, None, self.GetInstallPath() )
        self._InstallPipe += PackageUtil.ExecuteSimpleCommand( "make", [], None, self.GetInstallPath() )
        self._InstallPipe += PackageUtil.ExecuteSimpleCommand( "make", ['install'], None, self.GetInstallPath() )
        return
