using NUnit.Framework;
using Moq;
using PackageManager.Core;
using PackageManager.Core.Contracts;
using PackageManager.Models.Contracts;
using PackageManager.Enums;
using System.Collections.Generic;

namespace PackageManager.IntegrationTests.Core
{
    [TestFixture]
    public class PackageInstallerIntegrationTests
    {
        private Mock<IManager> mockManager;
        private Mock<IProject> mockProject;
        private Mock<IRepository<IPackage>> mockRepo;

        private PackageDownloader downloader;
        private PackageInstaller installer;

        [SetUp]
        public void SetUp()
        {
            mockManager = new Mock<IManager>();

            downloader = new PackageDownloader(mockManager.Object);

            mockProject = new Mock<IProject>();
            mockRepo = new Mock<IRepository<IPackage>>();

            mockProject.Setup(p => p.Location).Returns(@"C:\test-project");
            mockProject.Setup(p => p.PackageRepository).Returns(mockRepo.Object);

            mockRepo.Setup(r => r.GetAll()).Returns(new List<IPackage>());

            installer = new PackageInstaller(downloader, mockProject.Object);
        }

        [Test]
        public void Install_PerformsDownloadAndRemoveThroughDownloader()
        {
            // Arrange
            var mockPackage = new Mock<IPackage>();
            mockPackage.Setup(p => p.Name).Returns("example-package");
            mockPackage.Setup(p => p.Url).Returns("url");
            mockPackage.Setup(p => p.Dependencies).Returns(new List<IPackage>());

            installer.Operation = InstallerOperation.Install;

            // Act
            installer.PerformOperation(mockPackage.Object);

            // Assert
            mockManager.Verify(s => s.Delete(@"C:\test-project\my_modules\example-package"), Times.Once);
            mockManager.Verify(s => s.Create(@"C:\test-project\my_modules\example-package"), Times.Once);
            mockManager.Verify(s => s.Create(@"C:\test-project\my_modules\example-package\url"), Times.Once);

            mockRepo.Verify(r => r.Add(mockPackage.Object), Times.Once);
        }

        [Test]
        public void Uninstall_PerformsRemoveThroughDownloader()
        {
            // Arrange
            var mockPackage = new Mock<IPackage>();
            mockPackage.Setup(p => p.Name).Returns("example-package");
            mockPackage.Setup(p => p.Dependencies).Returns(new List<IPackage>());

            mockRepo.Setup(r => r.Delete(mockPackage.Object)).Returns(true);

            installer.Operation = InstallerOperation.Uninstall;

            // Act
            installer.PerformOperation(mockPackage.Object);

            // Assert
            mockManager.Verify(s => s.Delete(@"C:\test-project\my_modules\example-package"), Times.Once);
            mockRepo.Verify(r => r.Delete(mockPackage.Object), Times.Once);
        }
    }
}
