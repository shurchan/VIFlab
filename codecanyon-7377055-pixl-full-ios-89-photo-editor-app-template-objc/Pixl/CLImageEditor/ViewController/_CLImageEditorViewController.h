/*=====================
 -- Pixl --
 
 Created for CodeCanyon
 by FV iMAGINATION
 =====================*/

#import <iAd/iAd.h>
#import <AudioToolbox/AudioToolbox.h>
#import <GoogleMobileAds/GoogleMobileAds.h>


#import "CLImageEditor.h"

@interface _CLImageEditorViewController : CLImageEditor <
UIScrollViewDelegate,
UIBarPositioningDelegate,
GADBannerViewDelegate, ADBannerViewDelegate
>
{
    IBOutlet __weak UINavigationBar *_navigationBar;
    IBOutlet __weak UIScrollView *_scrollView;
}

//Ad banners properties
@property (strong, nonatomic) ADBannerView *iAdBannerView;
@property (strong, nonatomic) GADBannerView *adMobBannerView;


@property (nonatomic, strong) UIImageView  *imageView;
@property (nonatomic, weak) IBOutlet UIScrollView *menuView;
@property (nonatomic, readonly) UIScrollView *scrollView;


- (IBAction)pushedCloseBtn:(id)sender;
- (IBAction)pushedFinishBtn:(id)sender;


- (id)initWithImage:(UIImage*)image;


- (void)fixZoomScaleWithAnimated:(BOOL)animated;
- (void)resetZoomScaleWithAnimated:(BOOL)animated;

@end
