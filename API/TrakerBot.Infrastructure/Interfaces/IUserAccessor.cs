using TrakerBot.Core.Entities;
using TrakerBot.Infrastructure.UserInfo;

namespace TrakerBot.Infrastructure.Interfaces;

public interface IUserAccessor
{
    string GetUserId();
    Task<UserInfoDto> GetUserAsync();
    Task<ApplicationUser> GetUserWithPhotosAsync();
    string GetUserRoleNameByUserIdAsync(string userId);
}
