using NUnit.Framework;
using PackageManager.Models;
using PackageManager.Models.Contracts;
using PackageManager.Enums;

namespace PackageManager.UnitTests.Models
{
    [TestFixture]
    public class PackageTests
    {
        [Test]
        public void CompareTo_WhenVersionsAreEqual_ReturnsZero()
        {
            // Arrange
            var version1 = new PackageVersion(1, 0, 0, VersionType.final);
            var version2 = new PackageVersion(1, 0, 0, VersionType.final);
            var package1 = new Package("test", version1);
            var package2 = new Package("test", version2);

            // Act
            var result = package1.CompareTo(package2);

            // Assert
            Assert.That(result, Is.EqualTo(0));
        }

        [Test]
        public void CompareTo_WhenCurrentVersionIsGreater_ReturnsOne()
        {
            // Arrange
            var version1 = new PackageVersion(2, 0, 0, VersionType.final);
            var version2 = new PackageVersion(1, 0, 0, VersionType.final);
            var package1 = new Package("test", version1);
            var package2 = new Package("test", version2);

            // Act
            var result = package1.CompareTo(package2);

            // Assert
            Assert.That(result, Is.EqualTo(1));
        }

        [Test]
        public void CompareTo_WhenCurrentVersionIsLower_ReturnsMinusOne()
        {
            // Arrange
            var version1 = new PackageVersion(1, 0, 0, VersionType.final);
            var version2 = new PackageVersion(2, 0, 0, VersionType.final);
            var package1 = new Package("test", version1);
            var package2 = new Package("test", version2);

            // Act
            var result = package1.CompareTo(package2);

            // Assert
            Assert.That(result, Is.EqualTo(-1));
        }

        [Test]
        public void CompareTo_WhenPackageNamesDiffer_ThrowsArgumentException()
        {
            // Arrange
            var version1 = new PackageVersion(1, 0, 0, VersionType.final);
            var version2 = new PackageVersion(1, 0, 0, VersionType.final);
            var package1 = new Package("test1", version1);
            var package2 = new Package("test2", version2);

            // Act & Assert
            Assert.Throws<ArgumentException>(() => package1.CompareTo(package2));
        }

        [Test]
        public void CompareTo_WhenOtherIsNull_ThrowsArgumentNullException()
        {
            // Arrange
            var version = new PackageVersion(1, 0, 0, VersionType.final);
            var package = new Package("test", version);

            // Act & Assert
            Assert.Throws<ArgumentNullException>(() => package.CompareTo(null));
        }

        [Test]
        public void CompareTo_WithDifferentVersionTypes_ComparesCorrectly()
        {
            // Arrange
            var version1 = new PackageVersion(1, 0, 0, VersionType.final);
            var version2 = new PackageVersion(1, 0, 0, VersionType.beta);
            var package1 = new Package("test", version1);
            var package2 = new Package("test", version2);

            // Act
            var result = package1.CompareTo(package2);

            // Assert
            Assert.That(result, Is.EqualTo(1)); // final > beta
        }
    }
}