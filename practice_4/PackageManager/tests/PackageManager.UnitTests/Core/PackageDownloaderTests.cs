using NUnit.Framework;
using Moq;
using PackageManager.Core;
using PackageManager.Core.Contracts;

namespace PackageManager.UnitTests.Core
{
    [TestFixture]
    public class PackageDownloaderTests
    {
        [Test]
        public void Download_WithValidUrl_CallsSaverCreate()
        {
            // Arrange
            var mockSaver = new Mock<IManager>();
            var downloader = new PackageDownloader(mockSaver.Object);
            downloader.Location = @"C:\test";
            string url = "test-package";

            // Act
            downloader.Download(url);

            // Assert
            mockSaver.Verify(s => s.Create(@"C:\test\test-package"), Times.Once);
        }

        [Test]
        public void Remove_WithValidName_CallsSaverDelete()
        {
            // Arrange
            var mockSaver = new Mock<IManager>();
            var downloader = new PackageDownloader(mockSaver.Object);
            downloader.Location = @"C:\test";
            string name = "test-package";

            // Act
            downloader.Remove(name);

            // Assert
            mockSaver.Verify(s => s.Delete(@"C:\test\test-package"), Times.Once);
        }
    }
}