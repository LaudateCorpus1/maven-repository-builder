
"""maven_artifact.py Python code representing a Maven artifact"""

import logging
import re
import sys


class MavenArtifact:

    def __init__(self, groupId, artifactId, type, version):
        self.groupId = groupId
        self.artifactId = artifactId
        self.type = type
        self.version = version

    @staticmethod
    def createFromGAV(gav):
        """
        Initialize an artifact using a colon separated
        GAV of the form groupId:artifactId:[type:][classifier:]version[:scope]

        :returns: MavenArtifact instance
        """
        regexGAV =\
            re.compile('([\w._-]+):([\w._-]+):(?:([\w._-]+)?:)?([\w._-]+:)?([\d][\w._-]*)(:[\w._-]+)?')
        gavParts = regexGAV.search(gav)
        if gavParts is None:
            logging.error("Invalid GAV string: %s", gav)
            sys.exit(1)
        return MavenArtifact(gavParts.group(1), gavParts.group(2), gavParts.group(3), gavParts.group(5))

    def getDirPath(self):
        """Get the relative repository path to the artifact"""
        relativePath = self.groupId.replace('.', '/') + '/'
        relativePath += self.artifactId + '/'
        relativePath += self.version + '/'
        return relativePath

    def getGA(self):
        return self.groupId + ":" + self.artifactId

    def getBaseFilename(self):
        """Returns the filename without the file extension"""
        baseFilename = self.artifactId + '-' + self.version
        return baseFilename

    def getPomFilename(self):
        """Returns the filename of the pom file for this artifact"""
        return self.getBaseFilename() + '.pom'

    def getPomFilepath(self):
        """Return the path to the artifact file"""
        return self.getDirPath() + '/' + self.getPomFilename()

    def getSourcesFilename(self):
        """Returns the filename of the sources artifact"""
        return self.getBaseFilename() + '-sources.jar'

    def getSourcesFilepath(self):
        """Return the path to the artifact file"""
        return self.getDirPath() + '/' + self.getSourcesFilename()

    def __str__(self):
        result = self.groupId + ':' + self.artifactId
        if self.type:
            result += ':' + self.type
        result += ':' + self.version
        return result
