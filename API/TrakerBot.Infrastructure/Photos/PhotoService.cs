using CloudinaryDotNet;
using CloudinaryDotNet.Actions;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Options;
using TrakerBot.Infrastructure.DTOs;
using TrakerBot.Infrastructure.Interfaces;

namespace TrakerBot.Infrastructure.Photos;

public class PhotoService : IPhotoService
{
    private readonly Cloudinary _cloudinary;

    public PhotoService(IOptions<CloudinarySettings> cloudinarySettings)
    {
        var account = new Account(
            cloudinarySettings.Value.CloudName,
            cloudinarySettings.Value.ApiKey,
            cloudinarySettings.Value.ApiSecret
        );

        _cloudinary = new Cloudinary(account);
    }
    
    public async Task<string> DeletePhoto(string publicId)
    {
        var deleteParams = new DeletionParams(publicId);

        var result = await _cloudinary.DestroyAsync(deleteParams);

        if (result.Error != null)
        {
            throw new Exception(result.Error.Message);
        }

        return result.Result == "ok" ? "Photo deleted successfully" : "Photo deletion failed";
    }

    public async Task<PhotoUploadResult?> UpLoadPhoto(IFormFile file)
    {
        if (file.Length > 0)
        {
            await using var stream = file.OpenReadStream();

            var uploadParams = new ImageUploadParams
            {
                File = new FileDescription(file.FileName, stream),
                // Transformation = new Transformation().Width(500).Height(500).Crop("fill").Gravity("face")
                Folder = "BetBoard/Photos",
            };

            var uploadResult = await _cloudinary.UploadAsync(uploadParams);

            if (uploadResult.Error != null)
            {
                throw new Exception(uploadResult.Error.Message);
            }

            return new PhotoUploadResult
            {
                Url = uploadResult.SecureUrl.AbsoluteUri,
                PublicId = uploadResult.PublicId
            };
        }

        return null;;
    }
}
